from enum import IntEnum

from .hap_client import HapClient, HapSemaphore
from .model import *


class Device:
    def __init__(self, did, mac, name, zone):
        self.did = did
        self.mac = mac
        self.name = name
        self.zone = zone


class HomeClient(HapClient):
    def __init__(self, ip: str, password: str):
        self.entities = []
        self.scenes = []
        super().__init__(ip, password, self.on_message, self.on_close)

    def set_scene(self, sid: int):
        self.semamphore = HapSemaphore()
        self.send({"method": "set-scenes", "scenes": [{"sid": sid}]})
        self.semamphore.acquire(2)

    def set_attribute(self, did: int, sid: int, typ: int, value):
        self.semamphore = HapSemaphore()
        self.send(
            {
                "method": "set-attributes",
                "attributes": [{"did": did, "sid": sid, "type": typ, "value": value}],
            }
        )
        self.semamphore.acquire(2)

    def get_home(self):
        self.semamphore = HapSemaphore()
        self.send({"method": "get-home"})
        self.semamphore.acquire(5)

    def on_message(self, message):
        method = message["method"]
        if method == "response":
            if message["client"] == "get-home":
                self.home = message
                self._create_home_model()
            self.semamphore.release()

    def _create_home_model(self):
        self.entities = []
        self.scenes = []

        for device in self.home["devices"]:
            for service in device["services"]:

                did, reachable, zone, service_type, sid = (
                    device["did"],
                    device["reachable"],
                    self._find_zone(device["zid"]),
                    service["type"],
                    service["sid"],
                )
                if service_type in services_map:
                    args = (
                        self,
                        service_type,
                        Device(did, device["mac"], device["name"], zone),
                        sid,
                        service["attributes"],
                        reachable,
                    )
                    self.entities.append(services_map[service_type](*args))

        for scene in self.home["scenes"]:
            sid = scene["sid"]
            self.scenes.append(Scene(self, scene["name"], sid))

    def _find_zone(self, zid):
        for zone in self.home["zones"]:
            if zone["zid"] == zid:
                return zone["name"]
        return "null"

    def on_close(self):
        pass


class Scene:
    def __init__(self, client, name, sid):
        self._client = client
        self.name = name
        self.sid = sid

    def set(self):
        self._client.set_scene(self.sid)


class Entity:
    def __init__(self, _type, client, device, sid, reachable):
        self.type = _type
        self._client = client
        self.name = device.name
        self.did = device.did
        self.mac = device.mac
        self.zone = device.zone
        self.sid = sid
        self.reachable = reachable

        self.changed_attrs = set()
        self.on_state_change = lambda entity, attrs: None
        self.on_reachable_change = lambda entity, reachable: None


class Light(Entity):
    class Mode(IntEnum):
        COLOR_TEMPERATURE = 0x00
        HSV = 0x01

    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self.supported_modes = []

        self._onoff = 0
        self._brightness = 0
        self._color_temperature = 0
        self._hsv = (0, 0, 0)
        self._color_mode = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.COLOR_TEMPERATURE:
                self._color_temperature = value
                self.supported_modes.append(Light.Mode.COLOR_TEMPERATURE)
            elif _type == AttrType.HSV:
                self._hsv = (value["hue"], value["saturation"], value["brightness"])
                self.supported_modes.append(Light.Mode.HSV)
            elif _type == AttrType.ONOFF:
                self._onoff = value
            elif _type == AttrType.BRIGHTNESS:
                self._brightness = value
            elif _type == AttrType.LIGHT_MODE:
                self._color_mode = value

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, value)

    @property
    def color_mode(self):
        return self._color_mode

    @color_mode.setter
    def color_mode(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.LIGHT_MODE, value)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.BRIGHTNESS, value)

    @property
    def color_temperature(self):
        return self._color_temperature

    @color_temperature.setter
    def color_temperature(self, value):
        self._client.set_attribute(
            self.did, self.sid, AttrType.COLOR_TEMPERATURE, value
        )

    @property
    def hsv(self):
        return self._hsv

    @hsv.setter
    def hsv(self, value):
        self._client.set_attribute(
            self.did,
            self.sid,
            AttrType.HSV,
            {"hue": value[0], "saturation": value[1], "brightness": value[2]},
        )

    def toggle(self):
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, 2)


class Switch(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._onoff = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.ONOFF:
                self._onoff = value

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, value)

    def toggle(self):
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, 2)


class Thermostat(Entity):
    class WorkMode(IntEnum):
        OFF = 0x00
        COOL = 0x01
        HEAT = 0x02
        FAN = 0x03
        AUTO = 0x04
        DRY = 0x05

    class FanSpeed(IntEnum):
        LOW = 0x00
        MIDDLE = 0x01
        HIGH = 0x02
        OFF = 0x03
        AUTO = 0x04

    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._onoff = 0
        self._temperature = 0
        self._work_mode = 0
        self._fan_speed = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.ONOFF:
                self._onoff = value
            elif _type == AttrType.TARGET_TEMPERATURE:
                self._temperature = value
            elif _type == AttrType.THERMOSTAT_TARGET_WORK_MODE:
                self._work_mode = value
            elif _type == AttrType.THERMOSTAT_TARGET_FAN_SPEED:
                self._fan_speed = value

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, value)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._client.set_attribute(
            self.did, self.sid, AttrType.TARGET_TEMPERATURE, value
        )

    @property
    def work_mode(self):
        return self._work_mode

    @work_mode.setter
    def work_mode(self, value):
        self._client.set_attribute(
            self.did, self.sid, AttrType.THERMOSTAT_TARGET_WORK_MODE, value
        )

    @property
    def fan_speed(self):
        return self._fan_speed

    @fan_speed.setter
    def fan_speed(self, value):
        self._client.set_attribute(
            self.did, self.sid, AttrType.THERMOSTAT_TARGET_FAN_SPEED, value
        )


class CardSwitch(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._onoff = 0
        self._card_insert_status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.ONOFF:
                self._onoff = value
            elif _type == AttrType.CARD_INSERT_STATUS:
                self._card_insert_status = value

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, value)

    @property
    def card_insert_status(self):
        return self._card_insert_status


class MotionSensor(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.MOTION_STATUS:
                self._status = value

    @property
    def status(self):
        return self._status


class Curtain(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._current_position = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.POSITION_CURRENT:
                self._current_position = value

    @property
    def position(self):
        return self._current_position

    @position.setter
    def position(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.POSITION_TARGET, value)


class Door(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._target_position = 0
        self._current_position = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.POSITION_CURRENT:
                self._current_position = value
            elif _type == AttrType.POSITION_TARGET:
                self._target_position = value

    @property
    def position(self):
        return self._target_position

    @position.setter
    def position(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.POSITION_TARGET, value)


class Desk(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._height = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.HEIGHT:
                self._height = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.HEIGHT, value)


class ContactSensor(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.CONTACT_STATUS:
                self._status = value

    @property
    def status(self):
        return self._status


class OccupancySensor(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.OCCUPANCY_DETECT:
                self._status = value

    @property
    def status(self):
        return self._status


class Battery(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, reachable)

        self._status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.BATTERY_LEVEL:
                self._battery_level = value
            elif _type == AttrType.STATUS_LOW_BATTERY:
                self._low_battery = value

    @property
    def battery_level(self):
        return self._battery_level

    @property
    def low_battery(self):
        return self._low_battery


services_map = {
    ServiceType.LIGHT: Light,
    ServiceType.SWITCH: Switch,
    ServiceType.THERMOSTAT: Thermostat,
    ServiceType.CARD_SWITCH: CardSwitch,
    ServiceType.MOTION_SENSOR: MotionSensor,
    ServiceType.CURTAIN: Curtain,
    ServiceType.DOOR: Door,
    ServiceType.DESK: Desk,
    ServiceType.CONTACT_SENSOR: ContactSensor,
    ServiceType.OCCUPANCY_SENSOR: OccupancySensor,
    ServiceType.BATTERY_SERVICE: Battery,
}


if __name__ == "__main__":
    client = HomeClient("192.168.31.114", "mxhaspwd")
    for i in range(100):
        print(f"Connecting")
        client.open()
        print("Connected")
        client.set_scene(13220 + i % 2)
        print("Closing")
        client.close()
        print("Closed")
