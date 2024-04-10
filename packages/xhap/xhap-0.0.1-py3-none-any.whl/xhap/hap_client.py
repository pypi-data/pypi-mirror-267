import os
import threading
import json
import hmac
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .ws_client import WebSocketClient


def aes_ctr_encrypt(key, iv, plaintext):
    # 创建 AES-CTR 密码器对象
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    # 加密明文
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext


def aes_ctr_decrypt(key, iv, ciphertext):
    # 创建 AES-CTR 解密器对象
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    # 解密密文
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext


class HapException(Exception):
    def __init__(self, reason):
        self.reason = reason
        super().__init__(self.reason)


class HapSemaphore(threading.Semaphore):
    def __init__(self):
        super().__init__(0)

    def acquire(self, timeout: float | None = None) -> bool:
        if not super().acquire(True, timeout):
            raise HapException("Timeout")


class HapClient:
    def __init__(self, ip, password, on_message, on_close):
        self.ip = ip
        self.password = password.encode()
        self.on_message = on_message
        self.on_close = on_close
        self.auth_key = hashlib.pbkdf2_hmac(
            "sha256", self.password, b"MxHAP-Salt", 1000, dklen=16
        )
        self.ws = WebSocketClient()
        self.ws.on_message = self.on_ws_message
        self.ws.on_close = self.on_ws_close

    def open(self):
        self.send_iv = 0
        self.recv_iv = 0
        self.send_seq = 0
        self.recv_seq = 0
        self.json_str = b""
        self.is_connected = False
        self.connect_semaphore = threading.Semaphore(0)
        self.ws.open(self.ip)
        self.a = os.urandom(16)
        self.ws.send(self.a)
        self.connect_semaphore.acquire(timeout=5)
        if not self.is_connected:
            raise HapException("Failed to connect")

    def close(self):
        self.ws.close()

    def send(self, obj):
        data = self.send_seq.to_bytes(4, "little") + b"\x01" + json.dumps(obj).encode()
        encrypted_data = aes_ctr_encrypt(
            self.session_key, self.send_iv.to_bytes(16, "big"), data
        )
        mic = hmac.new(self.session_key, encrypted_data, hashlib.sha256).digest()[:8]
        self.ws.send(encrypted_data + mic)
        self.send_seq += 1
        self.send_iv += 1

    def on_ws_message(self, message):
        if not self.is_connected:
            A, b = message[:16], message[16:]
            decrypted_A = aes_ctr_decrypt(
                self.auth_key, self.recv_iv.to_bytes(16, "big"), A
            )
            if decrypted_A != self.a:
                print("Auth failed")
                self.disconnect()
                return

            B = aes_ctr_encrypt(self.auth_key, self.send_iv.to_bytes(16, "big"), b)
            self.ws.send(B)

            self.session_key = hashlib.pbkdf2_hmac(
                "sha256", self.password, self.a + b, 1000, dklen=16
            )

            self.is_connected = True
            self.connect_semaphore.release()
        else:
            data, mic = message[:-8], message[-8:]
            if hmac.new(self.session_key, data, hashlib.sha256).digest()[:8] != mic:
                print("Invalid MIC")
                return

            decrypted_data = aes_ctr_decrypt(
                self.session_key, self.recv_iv.to_bytes(16, "big"), data
            )
            seq = int.from_bytes(decrypted_data[:4], "little")
            if seq != self.recv_seq:
                print(f"Invalid sequence number: {seq}")
                return

            fin, payload = decrypted_data[4], decrypted_data[5:]

            if fin:
                self.json_str += payload
                self.on_message(json.loads(self.json_str.decode()))
                self.json_str = b""
            else:
                self.json_str += payload

            self.recv_seq += 1
            self.recv_iv += 1

    def on_ws_close(self):
        self.connect_semaphore.release()
        if self.is_connected:
            self.on_close()


if __name__ == "__main__":
    from time import sleep

    client = HapClient(
        "192.168.31.114", "mxhaspwd", lambda x: print(x), lambda: print("Closed")
    )
    while True:
        client.open()
        print("Connected")
        client.send({"method": "get-home"})
        sleep(2)
        client.close()
