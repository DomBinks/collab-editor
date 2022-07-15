from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OhJUfTfM4igIiYsfnkOQ'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html') 

@socketio.on('box change')
def handle_box_change(json):
    print('Box changed')
    socketio.emit('update box', json)

@app.route('/download', methods=['POST'])
def download():
    download_path = "dynamic/download" + request.form['extension'] 
    print('Downloading: ' + download_path)
    # Need to add error detection logic with try and except
    file = open(download_path, "w")
    file.write(request.form['content'])
    file.close()
    return send_file(download_path, as_attachment=True)
    # Works for .hs files but not .py or .c - just displays a page with the code

if __name__ == '__main__':
    socketio.run(app, debug=True)