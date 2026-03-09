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


def is_port_open(port):
    try:
        with socket.create_connection((HOST, port), timeout=TIMEOUT):
            return True
    except (socket.timeout, socket.error):
        return False


@app.route("/java")
def java_status():
    return jsonify({"online": is_port_open(PORTS["java"])})


@app.route("/bedrock")
def bedrock_status():
    return jsonify({"online": is_port_open(PORTS["bedrock"])})


@app.route("/voicechat")
def voicechat_status():
    return jsonify({"online": is_port_open(PORTS["voicechat"])})


@app.route("/voting")
def voting_status():
    return jsonify({"online": is_port_open(PORTS["voting"])})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
