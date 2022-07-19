from flask import Flask, flash, redirect, render_template, request, send_file
from flask_socketio import SocketIO
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OhJUfTfM4igIiYsfnkOQ'
socketio = SocketIO(app)

current_users = {} # Numbers of users connected to each session 
current_conents = {} # Content of every session's text area 
current_ids = {} # Session each user is connected to  

#-----Routing-----
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/editor/<session_id>')
def editor(session_id):
    if session_id in current_users:
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
        if session_id not in current_users:
            break

    # Set up dictionary starting values
    current_users[session_id] = 0
    current_conents[session_id] = ''

    # Redirect the client to the editor page for the new session
    socketio.emit('redirect', {'page': '/editor/' + session_id})

    print('Starting new session with id ' + session_id)
    return

@socketio.on('connect to session')
def handle_connect_to_session(json):
    session_id = json['session_id']

    # Update dictionary values
    current_users[session_id] += 1
    current_ids[request.sid] = session_id

    # Updates the client's text area with the current session content
    socketio.emit('update text', {'session_id': session_id,
        'content': current_conents[session_id]})

    print('Connection to session ' + session_id + ' by ' + request.sid) 
    return

@socketio.on('text change')
def handle_box_change(json):
    # Stores the current content of the text area
    current_conents[json['session_id']] = json['content']

    # Tells other clients to update their text areas
    socketio.emit('update text', json)
    return

@socketio.on('disconnect')
def handle_disconnect():
    # If a user who is connected to a session disconnects
    if request.sid in current_ids:
        # Decrement the user count of the session
        current_users[current_ids[request.sid]] -= 1
        if current_users[current_ids[request.sid]] == 0:
            # Delete the session if there are no clients connected
            del current_users[current_ids[request.sid]] 
            del current_conents[current_ids[request.sid]]
        # Remove the user from the dictionary of connected users
        del current_ids[request.sid]

    print('Disconnection by ' + request.sid)
    return

#-----Run-----
if __name__ == '__main__':
    socketio.run(app)