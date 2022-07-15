from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OhJUfTfM4igIiYsfnkOQ'
socketio = SocketIO(app)

current_sessions = []

@app.errorhandler(404)
def error_page(_):
    return render_template('error.html'), 404

@app.route('/')
def index():
    return render_template('index.html') 

@socketio.on('box change')
def handle_box_change(json):
    print('Box changed')
    socketio.emit('update box', json)

@socketio.on('start session')
def handle_start_session():
    print('Starting new session')

    session_id = ''.join(str(randint(0, 9)) for _ in range(6))
    current_sessions.append(session_id)
    print('New session id: ' + session_id)

    socketio.emit('redirect', {'page': '/editor/' + session_id})
# Need to ensure session is closed once all clients have stopped connecting

@app.route('/editor/<session_id>')
def editor(session_id):
    if session_id in current_sessions:
        return render_template('editor.html')
    else:
        return render_template('error.html')

@app.route('/download', methods=['POST'])
def download():
    download_path = "dynamic/download" + request.form['extension'] 
    print('Downloading: ' + download_path)
    # Need to add error detection logic with try and except
    file = open(download_path, "w")
    file.write(request.form['content'])
    file.close()
    return send_file(download_path, as_attachment=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)