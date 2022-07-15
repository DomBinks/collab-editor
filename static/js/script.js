let socket = io();

function boxChange()
{
    let box = document.getElementById('text_area').value;
    socket.emit('box change', {data: box});
}

socket.on('update box', (json) => {
    document.getElementById('text_area').value = json['data'];
});

function startNewSession()
{
    socket.emit('start session')
}

socket.on('redirect', (json) => {
    window.location = json['page'];
});

function joinSession()
{
    window.location = '/editor/' + document.getElementById('join_id_text').value;
}

function returnToIndex()
{
    window.location = '/';
}