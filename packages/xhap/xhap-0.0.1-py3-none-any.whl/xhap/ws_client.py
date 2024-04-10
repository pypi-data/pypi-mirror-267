import socket
import base64
import threading


class WebSocketClient:
    def open(self, ip):
        # 创建 TCP 连接
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        self.sock.connect((ip, 53248))
        self.sock.settimeout(None)
        # 进行 WebSocket 握手
        self.handshake()
        # 创建接收线程
        self.thread = threading.Thread(target=self.recv_thread, daemon=True)
        self.thread.start()

    def handshake(self):
        handshake_request = (
            b"GET /ws HTTP/1.1\r\n"
            b"Upgrade: websocket\r\n"
            b"Connection: Upgrade\r\n"
            b"Sec-WebSocket-Key: " + base64.b64encode(b"websocket_key") + b"\r\n"
            b"Sec-WebSocket-Version: 13\r\n"
            b"\r\n"
        )
        self.sock.sendall(handshake_request)
        self.sock.recv(1024)

    # 接收指定长度的数据
    def recv(self, length):
        recved_data = b""
        while True:
            data = self.sock.recv(length)
            recved_data += data
            length -= len(data)
            if not length:
                break
        return recved_data

    def send(self, payload):
        opcode = 0x02  # Binary frame
        header = bytes([0x80 | opcode])  # FIN bit set to 1
        payload_len = len(payload)
        if payload_len <= 125:
            header += payload_len.to_bytes(1, "big")
        elif payload_len <= 65535:
            header += bytes([126]) + payload_len.to_bytes(2, "big")
        else:
            header += bytes([127]) + payload_len.to_bytes(8, "big")
        self.sock.sendall(header + payload)

    def recv_thread(self):
        try:
            while True:
                header = self.recv(2)
                payload_length = header[1] & 127
                if payload_length == 126:
                    payload_length = int.from_bytes(self.recv(2), "big")
                elif payload_length == 127:
                    payload_length = int.from_bytes(self.recv(8), "big")
                payload = bytearray(self.recv(payload_length))
                self.on_message(payload)
        except Exception as e:
            self.on_close()

    def close(self):
        self.sock.close()
        if threading.current_thread() != self.thread:
            self.thread.join()


if __name__ == "__main__":
    client = WebSocketClient()
    client.on_message = lambda payload: print(payload)
    client.on_close = lambda: print("Closed")
    from time import sleep

    while True:
        client.open("192.168.31.114")
        client.send(b"\x00" * 16)
        sleep(2)
        client.close()
