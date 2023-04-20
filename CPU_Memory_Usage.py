from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import psutil
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')
    

@socketio.on('connect')
def test_connect():
    print('Client connected')
    
    emit('server_response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('get_usage')
def get_usage():
    while True:
        socketio.sleep(1)
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        emit('server_system_info', {'cpu_usage': cpu_usage, 'memory_usage': memory_usage, 'disk_usage': disk_usage})

if __name__ == '__main__':
    webbrowser.open_new('http://localhost:5000/')
    socketio.run(app, debug=True)
