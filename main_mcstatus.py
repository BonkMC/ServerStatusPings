from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from mcstatus import JavaServer, BedrockServer

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"],
)

@app.route("/java")
def get_java_server_status():
    try:
        server = JavaServer.lookup("play.bonkmc.net:25565")
        status = server.status()
        return jsonify({
            "online": True,
            "players_online": status.players.online,
            "players_max": status.players.max,
            "latency_ms": status.latency
        })
    except Exception:
        return jsonify({"online": False})

@app.route("/bedrock")
def get_bedrock_server_status():
    try:
        server = BedrockServer.lookup("play.bonkmc.net:19132")
        status = server.status()
        return jsonify({
            "online": True,
            "players_online": status.players.online,
            "players_max": status.players.max,
            "latency_ms": status.latency
        })
    except Exception:
        return jsonify({"online": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
