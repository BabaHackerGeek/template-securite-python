import base64
import socket

from src.tp3.utils.config import logger


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def breach_network(host: str, port: int, key_hex: str, rounds: int = 3, timeout: float = 5.0) -> str:
    """Se connecte au service TCP, décode chaque round et répond à temps, renvoie le flag final."""
    key = bytes.fromhex(key_hex)

    with socket.create_connection((host, int(port)), timeout=timeout) as sock:
        sock.settimeout(timeout)
        buf = b""

        def recv_line():
            nonlocal buf
            while b"\n" not in buf:
                buf += sock.recv(1024)
            line, buf = buf.split(b"\n", 1)
            return line

        recv_line()  # ligne d'instructions, on l'ignore

        for i in range(rounds):
            token_b64 = recv_line()
            token = xor_bytes(base64.b64decode(token_b64), key)
            sock.sendall(token + b"\n")
            logger.info(f"Round {i + 1}/{rounds} résolu")

        final_line = recv_line().decode()
        return final_line.removeprefix("OK ").strip()
