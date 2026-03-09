from flask import Flask, jsonify
import socket

app = Flask(__name__)

HOST = "127.0.0.1"
TIMEOUT = 3

PORTS = {
    "java": 25565,
    "bedrock": 19132,
    "voicechat": 24454,
    "voting": 25563,
}


def is_tcp_port_open(port):
    try:
        with socket.create_connection((HOST, port), timeout=TIMEOUT):
            return True
    except (socket.timeout, socket.error):
        return False


def is_udp_port_open(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(TIMEOUT)
        sock.sendto(b'\x00', (HOST, port))
        sock.recvfrom(1024)
        return True
    except (socket.timeout, socket.error):
        return False
    finally:
        sock.close()


def is_votifier_running(port):
    try:
        with socket.create_connection((HOST, port), timeout=TIMEOUT) as conn:
            data = conn.recv(256).decode("utf-8", errors="ignore")
            return data.startswith("VOTIFIER")
    except (socket.timeout, socket.error):
        return False


@app.route("/java")
def java_status():
    return jsonify({"online": is_tcp_port_open(PORTS["java"])})


@app.route("/bedrock")
def bedrock_status():
    return jsonify({"online": is_tcp_port_open(PORTS["bedrock"])})


@app.route("/voicechat")
def voicechat_status():
    return jsonify({"online": is_udp_port_open(PORTS["voicechat"])})


@app.route("/voting")
def voting_status():
    return jsonify({"online": is_votifier_running(PORTS["voting"])})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
