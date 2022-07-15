let socket = io();

// When a new window opens it doesn't fill out existing content automatically
function boxChange()
{
    let box = document.getElementById('text_area').value;
    socket.emit('box change', {data: box});
}

socket.on('update box', function(json) {
    document.getElementById('text_area').value = json['data'];
});

function startNewSession()
{
    socket.emit('start session')
}

socket.on('redirect', function(json) {
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