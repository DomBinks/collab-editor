from flask import Flask, flash, redirect, render_template, request, send_file
from flask_socketio import SocketIO
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OhJUfTfM4igIiYsfnkOQ'
socketio = SocketIO(app)

session_contents = {} # Content of every session's text area 

#-----Routing-----
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/editor/<session_id>')
def editor(session_id):
    if session_id in session_contents:
        return render_template('editor.html', session_id=session_id)
    else:
        return render_template('error.html',
            message='Sorry but that session doesn\'t exist.')

@app.route('/download', methods=['POST'])
def download():
    # Setup the path to the local download file
    download_path = "dynamic/download" + request.form['extension'] 
    try:
        # Write the content of the text area to the file
        file = open(download_path, "w")
        file.write(request.form['content']) 
        file.close()
        # Send the file to be downloaded
        return send_file(download_path, as_attachment=True)
    except:
        # Use a flash so the client receives a error message
        flash('download error')
        # Redirect the client back to the editor
        return redirect(request.referrer)

#-----Error Handling-----
@app.errorhandler(404)
def handle_404(e):
    return render_template('error.html',
        message='Sorry but this page doesn\'t exist.'), 404

#-----Socket.IO Handling-----
@socketio.on('start session')
def handle_start_session():
    # Generate a new random session id
    while True:
        session_id = ''.join(str(randint(0, 9)) for _ in range(6))
        if session_id not in session_contents:
            break

    # Set up the dictionary that keeps track of the contents of the text area 
    session_contents[session_id] = ''

    # Redirect the client to the editor page for the new session
    socketio.emit('redirect', {'page': '/editor/' + session_id})

    print('Starting new session with id ' + session_id)
    return

@socketio.on('connect to session')
def handle_connect_to_session(json):
    session_id = json['session_id']

    # Updates the client's text area with the current session content
    socketio.emit('update text', {'session_id': session_id,
        'content': session_contents[session_id]})
    return

@socketio.on('text change')
def handle_box_change(json):
    # Stores the current content of the text area
    session_contents[json['session_id']] = json['content']

    # Tells other clients to update their text areas
    socketio.emit('update text', json)
    return

@socketio.on('close session')
def handle_close_session(json):
    # Delete the contents of the session's text area 
    del session_contents[json['session_id']]

    # Tells the client to go to the index page
    socketio.emit('index', json)

    print('Session with id ' + json['session_id'] + ' has been closed')
    return

#-----Run-----
if __name__ == '__main__':
    print('Starting server')
    socketio.run(app)