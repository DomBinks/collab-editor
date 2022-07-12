from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OhJUfTfM4igIiYsfnkOQ'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html') 

@socketio.on('get line')
def hand_add_line(json):
    print('Line submitted: ' + str(json))
    socketio.emit('add line', json)

if __name__ == '__main__':
    socketio.run(app, debug=True)