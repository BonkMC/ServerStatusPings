from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from mcstatus import JavaServer, BedrockServer
import threading
import time

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

cached_java_status = {
    "online": False,
    "players_online": 0,
    "players_max": 0,
    "latency_ms": None
}

cached_bedrock_status = {
    "online": False,
    "players_online": 0,
    "players_max": 0,
    "latency_ms": None
}

def update_java_status():
    global cached_java_status
    while True:
        try:
            server = JavaServer.lookup("play.bonkmc.net:25565")
            status = server.status(timeout=1.5)
            cached_java_status = {
                "online": True,
                "players_online": status.players.online,
                "players_max": status.players.max,
                "latency_ms": status.latency
            }
        except Exception:
            cached_java_status = {
                "online": False,
                "players_online": 0,
                "players_max": 0,
                "latency_ms": None
            }
        time.sleep(15)

def update_bedrock_status():
    global cached_bedrock_status
    while True:
        try:
            server = BedrockServer.lookup("play.bonkmc.net:19132")
            status = server.status(timeout=1.5)
            cached_bedrock_status = {
                "online": True,
                "players_online": status.players.online,
                "players_max": status.players.max,
                "latency_ms": status.latency
            }
        except Exception:
            cached_bedrock_status = {
                "online": False,
                "players_online": 0,
                "players_max": 0,
                "latency_ms": None
            }
        time.sleep(15)

@app.route("/health")
def health():
    return "ok", 200

@app.route("/java")
def get_java_server_status():
    return jsonify(cached_java_status)

@app.route("/bedrock")
def get_bedrock_server_status():
    return jsonify(cached_bedrock_status)

if __name__ == "__main__":
    threading.Thread(target=update_java_status, daemon=True).start()
    threading.Thread(target=update_bedrock_status, daemon=True).start()
    app.run(host="127.0.0.1", port=8000)