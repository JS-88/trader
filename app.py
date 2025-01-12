from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)
is_bot_running = False

def bot_thread():
    global is_bot_running
    while is_bot_running:
        socketio.emit('log', 'Bot is analyzing data...')
        time.sleep(2)
        socketio.emit('log', 'Bot executed a trade.')
        time.sleep(3)

@app.route('/start-bot', methods=['POST'])
def start_bot():
    global is_bot_running
    if not is_bot_running:
        is_bot_running = True
        threading.Thread(target=bot_thread).start()
        return jsonify({"status": "Bot started"}), 200
    return jsonify({"status": "Bot already running"}), 400

@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global is_bot_running
    is_bot_running = False
    return jsonify({"status": "Bot stopped"}), 200

@socketio.on('connect')
def handle_connect():
    socketio.emit('log', 'Connected to the bot log server.')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)
