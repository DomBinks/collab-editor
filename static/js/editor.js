let socket = io();

let id;

function boxChange(session_id)
{
    let box = document.getElementById('text_area').value;
    socket.emit('box change', {data: box, session_id: session_id});
}

socket.on('update box', (json) => {
    if (id == json['session_id']) {
        document.getElementById('text_area').value = json['data'];
    } 
});


function connectToSession(session_id)
{
    id = session_id;
    socket.emit('connect to session', {data: session_id});
}
