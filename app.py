from flask import Flask, flash, redirect, render_template, request, send_file
from flask_socketio import SocketIO
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OhJUfTfM4igIiYsfnkOQ'
socketio = SocketIO(app)

current_sessions = {} # Keeps track of number of users per session
current_ids = {} # Keeps track of which user is in which session

@app.errorhandler(404)
def handle_404(e):
    return render_template('error.html'), 404

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/editor/<session_id>')
def editor(session_id):
    if session_id in current_sessions:
        return render_template('editor.html', session_id=session_id)
    else:
        return render_template('error.html')

@app.route('/download', methods=['POST'])
def download():
    download_path = "dynamic/download" + request.form['extension'] 
    try:
        file = open(download_path, "w")
        file.write(request.form['content']) 
        file.close()
        return send_file(download_path, as_attachment=True)
    except:
        print('Error when downloading ' + download_path)
        flash('download error')
        return redirect(request.referrer)

@socketio.on('box change')
def handle_box_change(json):
    socketio.emit('update box', json)

@socketio.on('start session')
def handle_start_session():
    while True:
        session_id = ''.join(str(randint(0, 9)) for _ in range(6))
        if session_id not in current_sessions:
            break

    current_sessions[session_id] = 0 
    print('Starting new session with id ' + session_id)

    socketio.emit('redirect', {'page': '/editor/' + session_id})

@socketio.on('connect')
def handle_connect():
    print('New connection by ' + request.sid)

@socketio.on('connect to session')
def handle_connect_to_session(json):
    session_id = str(json['data'])
    print('Connection to session ' + session_id + ' by ' + request.sid) 
    print('Adding ' + request.sid + ' to current_ids')
    current_ids[request.sid] = session_id
    current_sessions[session_id] += 1

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnection by ' + request.sid)
    if request.sid in current_ids:
        print('Removing ' + request.sid + ' from current_ids')
        current_sessions[current_ids[request.sid]] -= 1
        if current_sessions[current_ids[request.sid]] == 0:
            del current_sessions[current_ids[request.sid]] 
        del current_ids[request.sid]

if __name__ == '__main__':
    socketio.run(app, debug=True)