from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from db import get_stats, init_db
import threading
import time
import os

app = Flask(__name__, 
            template_folder="../frontend",
            static_folder="../frontend",
            static_url_path="")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()

def push_stats():
    """Push live stats to frontend every 2 seconds"""
    while True:
        stats = get_stats()
        socketio.emit("stats_update", stats)
        time.sleep(2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def stats():
    return jsonify(get_stats())

@socketio.on("connect")
def on_connect():
    print("[+] Client connected")
    emit("stats_update", get_stats())

if __name__ == "__main__":
    # Start background stats pusher
    t = threading.Thread(target=push_stats, daemon=True)
    t.start()
    print("[*] Dashboard at http://localhost:5000")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)