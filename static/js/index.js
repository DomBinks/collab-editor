let socket = io();

function startNewSession()
{
    socket.emit('start session');
}

function joinSession()
{
    window.location = '/editor/' + document.getElementById('join_id_text').value;
}

socket.on('redirect', (json) => {
    window.location = json['page'];
});