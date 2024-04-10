import json
import click
from rich.console import Console
from rich.table import Table
from rich import box
from typing import Union, Any

from .browser import Browser
from .home_client import HomeClient

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def get_version():
    from pkg_resources import get_distribution

    return get_distribution("xhap").version


def print_version(
    context: click.Context, param: Union[click.Option, click.Parameter], value: bool
) -> Any:
    """Print the version of mbed-tools."""
    if not value or context.resilient_parsing:
        return
    click.echo(get_version())
    context.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Display versions.",
)
def cli() -> None:
    """The MXCHIP Home Access Client Tool."""
    pass


@click.command()
def scan() -> None:
    """Scan for MxHAS on local network.

    Example:

        $ xhap scan
    """
    browser = Browser()
    click.echo("Scanning for servers ...")
    browser.scan()

    if len(browser.servers) == 0:
        click.echo("No server found")
        return

    table = Table(title="Servers", box=box.ROUNDED)
    table.add_column("Name")
    table.add_column("Model")
    table.add_column("MAC")
    table.add_column("IP")
    for _, server in enumerate(browser.servers):
        table.add_row(server.name, server.model, server.mac, f"{server.ip}")
    console = Console()
    console.print(table)


@click.command()
@click.argument("ip", type=click.STRING)
@click.argument("password", type=click.STRING, default="mxhaspwd")
@click.option("-s", "--save", type=click.STRING)
def info(ip: str, password: str, save: str) -> None:
    """Connect to HAS and Get Home model.

    Arguments:

        IP: IPv4 address. eg, 192.168.31.66

        PASSWORD: Password of the server, default is "mxhaspwd".

        -s/--save: save the home model to a file in JSON format.

    Example:

        $ xhap info 192.168.31.66 mxhaspwd
    """

    click.echo(f"Connecting to {ip} ...")
    client = HomeClient(ip, password)

    try:
        client.open()
        client.get_home()
    except Exception as e:
        click.echo(f"{e}")
        return

    if save:
        with open(save, "w") as f:
            f.write(json.dumps(client.home, indent=2, ensure_ascii=False))
        return

    console = Console()

    table = Table(title="Entities", box=box.ROUNDED)
    table.add_column("Name")
    table.add_column("Room")
    table.add_column("MAC")
    for entity in client.entities:
        table.add_row(f"{entity.name}-{entity.sid}", entity.zone, entity.mac)
    console.print(table)

    table = Table(title="Scenes", box=box.ROUNDED)
    table.add_column("Name")
    for scene in client.scenes:
        table.add_row(scene.name)
    console.print(table)


@click.command()
@click.argument("ip", type=click.STRING)
@click.argument("password", type=click.STRING)
@click.argument("did", type=click.INT)
@click.argument("sid", type=click.INT)
@click.argument("typ", type=click.INT)
@click.argument("value", type=click.INT)
def attr(ip: str, password: str, did: int, sid: int, typ: int, value: int) -> None:
    """Connect to HAS and set attribute

    Arguments:

        IP: IPv4 address. eg, 192.168.31.66

        PASSWORD: Password of the server, default is "mxhaspwd".

        DID: Device ID.

        SID: Service ID.

        typ: Type of the attribute.

        VALUE: Value of the attribute.

    Example:

        $ xhap attr 192.168.31.66 mxhaspwd 66 0 256 1
    """

    click.echo(f"Connecting to {ip} ...")
    client = HomeClient(ip, password)
    try:
        client.open()
        click.echo("Setting attribute ...")
        client.set_attribute(did, sid, typ, value)
    except Exception as e:
        click.echo(f"{e}")


@click.command()
@click.argument("ip", type=click.STRING)
@click.argument("password", type=click.STRING)
@click.argument("sid", type=click.INT)
def scene(ip: str, password: str, sid: int) -> None:
    """Connect to HAS and set scene

    Arguments:

        IP: IPv4 address. eg, 192.168.31.66

        PASSWORD: Password of the server, default is "mxhaspwd".

        SID: Scene ID.

    Example:

        $ xhap scene 192.168.31.66 mxhaspwd 6
    """

    click.echo(f"Connecting to {ip} ...")
    client = HomeClient(ip, password)
    try:
        client.open()
        click.echo("Setting scene ...")
        client.set_scene(sid)
    except Exception as e:
        click.echo(f"{e}")


def main():
    cli.add_command(scan, "scan")
    cli.add_command(info, "info")
    cli.add_command(attr, "attr")
    cli.add_command(scene, "scene")
    cli()


if __name__ == "__main__":
    main()
