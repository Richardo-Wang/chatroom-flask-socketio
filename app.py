from flask import Flask, render_template, redirect, session, request, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO()
socketio.init_app(app)

online_user = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('chatroom'))
        return render_template('login.html')
    else:
        username = request.form.get('username')
        session['username'] = username
        return redirect(url_for('chatroom'))

@app.route('/chatroom')
def chatroom():
    if 'username' in session:
        username = session['username']
        return render_template('chatroom.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
    return redirect(url_for("login"))

@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    online_user.append(username)
    print(f'{username} connect')
    socketio.emit('connect info', f'{username} connect')

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    print(f'{username} disconnect')
    socketio.emit('connect info', f'{username} disconnect')

@socketio.on('connect info')
def handle_connect_info(info):
    print('connect info'+str(info))
    socketio.emit('connect info', info)

@socketio.on('send msg')
def send_msg(data):
    print('Msg:'+str(data))
    socketio.emit('send msg', data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
