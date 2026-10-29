import base64
import socket
import threading

from src.tp3.utils.network import breach_network, xor_bytes


def test_xor_bytes_est_reversible():
    # Given
    data = b"abc"
    key = b"\x01"

    # When
    chiffre = xor_bytes(data, key)

    # Then
    assert chiffre == bytes(b ^ 1 for b in data)
    assert xor_bytes(chiffre, key) == data


def test_breach_network_resout_un_round(monkeypatch):
    # Given : un faux serveur TCP local qui suit le protocole du TP3
    key = bytes.fromhex("deadbeef")
    token = b"abcdef0123456789"

    def faux_serveur(srv):
        conn, _ = srv.accept()
        conn.sendall(b"instructions\n")
        conn.sendall(base64.b64encode(xor_bytes(token, key)) + b"\n")
        reponse = conn.recv(1024).strip()
        assert reponse == token
        conn.sendall(b"OK ESGI{chain_test}\n")
        conn.close()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    threading.Thread(target=faux_serveur, args=(srv,), daemon=True).start()

    # When
    result = breach_network("127.0.0.1", port, key.hex(), rounds=1)

    # Then
    assert result == "ESGI{chain_test}"
