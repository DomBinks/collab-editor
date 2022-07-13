let socket = io();

function boxChange()
{
    let box = document.getElementById('text_area').value;
    socket.emit('box change', {data: box});
}

socket.on('update box', function(json) {
    document.getElementById('text_area').value = json['data'];
});