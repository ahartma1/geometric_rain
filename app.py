from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
from src.geometric_rain.main import run_game

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('webrtc_signal')
def handle_webrtc_signal(data):
    emit('webrtc_signal', data, broadcast=True)

def start_game():
    run_game()

if __name__ == '__main__':
    threading.Thread(target=start_game).start()
    socketio.run(app, host='0.0.0.0', port=5000)