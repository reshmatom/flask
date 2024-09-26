
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
socketio = SocketIO(app)

# Route to serve the chat application
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event to handle messages
@socketio.on('message')
def handle_message(msg):
    print(f"Message received: {msg}")  # Log the received message
    emit('response', msg, broadcast=True)  # Broadcast the message to all connected clients

if __name__ == '__main__':
    socketio.run(app, debug=True)
