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


class GatewayException(Exception):
    def __init__(self, reason):
        self.reason = reason
        super().__init__(self.reason)


class GatewaySemaphore(threading.Semaphore):
    def __init__(self):
        super().__init__(0)

    def acquire(self, timeout: float | None = None) -> bool:
        if not super().acquire(True, timeout):
            raise GatewayException("Timeout")


class GatewayClient:
    def __init__(self):
        self._ws = WebSocketClient()
        self._ws.on_message = self._on_ws_message
        self._ws.on_close = self._on_ws_close

    def open(self, ip, password):

        self._password = password.encode()

        self._send_iv = 0
        self._recv_iv = 0
        self._send_seq = 0
        self._recv_seq = 0
        self._auth_key = hashlib.pbkdf2_hmac(
            "sha256", self._password, b"mxchip-gateway-salt", 1000, dklen=16
        )

        self._message = b""
        self._is_connected = False
        self._connect_semaphore = threading.Semaphore(0)

        self._ws.open(ip)
        self._a = os.urandom(16)
        self._ws.send(self._a)
        self._connect_semaphore.acquire(timeout=5)
        if not self._is_connected:
            raise GatewayException("Failed to connect")

    def close(self):
        self._ws.close()

    def send(self, obj):
        data = self._send_seq.to_bytes(4, "little") + b"\x01" + json.dumps(obj).encode()
        encrypted_data = aes_ctr_encrypt(
            self.session_key, self._send_iv.to_bytes(16, "big"), data
        )
        mic = hmac.new(self.session_key, encrypted_data, hashlib.sha256).digest()[:8]
        self._ws.send(encrypted_data + mic)
        self._send_seq += 1
        self._send_iv += 1

    def _on_ws_message(self, message):
        if not self._is_connected:
            A, b = message[:16], message[16:]
            decrypted_A = aes_ctr_decrypt(
                self._auth_key, self._recv_iv.to_bytes(16, "big"), A
            )
            if decrypted_A != self._a:
                print("Auth failed")
                self.disconnect()
                return

            B = aes_ctr_encrypt(self._auth_key, self._send_iv.to_bytes(16, "big"), b)
            self._ws.send(B)

            self.session_key = hashlib.pbkdf2_hmac(
                "sha256", self._password, self._a + b, 1000, dklen=16
            )

            self._is_connected = True
            self._connect_semaphore.release()
        else:
            data, mic = message[:-8], message[-8:]
            if hmac.new(self.session_key, data, hashlib.sha256).digest()[:8] != mic:
                print("Invalid MIC")
                return

            decrypted_data = aes_ctr_decrypt(
                self.session_key, self._recv_iv.to_bytes(16, "big"), data
            )
            seq = int.from_bytes(decrypted_data[:4], "little")
            if seq != self._recv_seq:
                print(f"Invalid sequence number: {seq}")
                return

            fin, payload = decrypted_data[4], decrypted_data[5:]

            if fin:
                self._message += payload
                self.on_message(json.loads(self._message.decode()))
                self._message = b""
            else:
                self._message += payload

            self._recv_seq += 1
            self._recv_iv += 1

    def _on_ws_close(self):
        self._connect_semaphore.release()
        if self._is_connected:
            self.on_close()


if __name__ == "__main__":
    from time import sleep

    client = GatewayClient()
    client.on_message = lambda message: print(message)
    client.on_close = lambda: print("Closed")
    while True:
        client.open("192.168.31.114", "mxchip-gateway-admin")
        print("Connected")
        client.send({"method": "get-home"})
        sleep(2)
        client.close()
