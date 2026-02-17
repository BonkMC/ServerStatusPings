from flask import Flask, jsonify
import socket

app = Flask(__name__)

def check_java_server(host, port=25565, timeout=5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False

def check_bedrock_server(host, port=19132, timeout=5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.sendto(b'\x01', (host, port))
        sock.recvfrom(1024)
        return True
    except Exception:
        return False

@app.route("/java")
def get_java_server_status():
    return jsonify({
        "online": check_java_server("play.bonkmc.net", 25565)
    })

@app.route("/bedrock")
def get_bedrock_server_status():
    return jsonify({
        "online": check_bedrock_server("play.bonkmc.net", 19132)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
