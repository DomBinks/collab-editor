let socket = io();
let id; // Stores the current session id

// Notifies the server that a new connection to the session has been made
function connectToSession(session_id)
{
    id = session_id;
    socket.emit('connect to session', {'session_id': session_id});
}

// Notifies the server that the text area has been changed
function textChange()
{
    let content = document.getElementById('text-area').value;
    socket.emit('text change', {'session_id': id, 'content': content});
}

// Tells the server to close the current session
function closeSession()
{
    socket.emit('close session', {'session_id': id});
}

// Updates the text area when it is changed by another client
socket.on('update text', (json) => {
    // Checks to make sure the change is for the session the client is in
    if (id == json['session_id']) {
        document.getElementById('text-area').value = json['content'];
    } 
});

// Moves the client to the index page 
socket.on('index', (json) => {
    if (id == json['session_id']) {
        window.location = '/';
    }
});