from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OhJUfTfM4igIiYsfnkOQ'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html') 

@socketio.on('box change')
def handle_box_change(json):
    print('Box changed')
    socketio.emit('update box', json)

if __name__ == '__main__':
    socketio.run(app, debug=True)