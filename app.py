from flask import Flask, flash, redirect, render_template, request, send_file
from flask_socketio import SocketIO
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OhJUfTfM4igIiYsfnkOQ'
socketio = SocketIO(app)

current_sessions = []

@app.errorhandler(404)
def handle_404(e):
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

@app.route('/editor/<session_id>')
def editor(session_id):
    if session_id in current_sessions:
        return render_template('editor.html', session_id=session_id)
    else:
        return render_template('error.html')

@app.route('/download', methods=['POST'])
def download():
    download_path = "dynamic/download" + request.form['extension'] 
    print('Downloading: ' + download_path)
    try:
        file = open(download_path, "w")
        file.write(request.form['content'])
        file.close()
        return send_file(download_path, as_attachment=True)
    except:
        print('Error when downloading: ' + download_path)
        flash('download error')
        return redirect(request.referrer)

if __name__ == '__main__':
    socketio.run(app, debug=True)