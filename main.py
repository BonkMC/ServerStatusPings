from flask import Flask, jsonify
import socket

app = Flask(__name__)

# this is shit and repetitive but idgaf

HOST = "127.0.0.1"
TIMEOUT = 3

PORTS = {
    "java": 25565,
    "bedrock": 19132,
    "voting": 25563,
    "lobby": 25560,
    "survival": 25561,
    "databases": 3306,
}


def is_tcp_port_open(port):
    try:
        with socket.create_connection((HOST, port), timeout=TIMEOUT):
            return True
    except (socket.timeout, socket.error):
        return False


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


@app.route("/voting")
def voting_status():
    return jsonify({"online": is_votifier_running(PORTS["voting"])})


@app.route("/lobby")
def lobby_status():
    return jsonify({"online": is_tcp_port_open(PORTS["lobby"])})


@app.route("/survival")
def survival_status():
    return jsonify({"online": is_tcp_port_open(PORTS["survival"])})

@app.route("/databases")
def databases_status():
    return jsonify({"online": is_tcp_port_open(PORTS["databases"])})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
