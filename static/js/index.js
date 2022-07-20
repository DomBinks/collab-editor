let socket = io();

// Called when the start new session button is clicked
function startSession()
{
    socket.emit('start session');
}

// Called when the join session button is clicked
function joinSession()
{
    // Sends the client to the page for the editor with the provided session id
    // If the session doesn't exist a 404 page will be served to the client
    window.location = '/editor/' + document.getElementById('join').value;
}

// Redirects the client to the page for the newly created session
socket.on('redirect', (json) => {
    window.location = json['page'];
});