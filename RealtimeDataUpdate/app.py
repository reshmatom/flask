from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import random
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
socketio = SocketIO(app)

# Route to serve the real-time update page
@app.route('/')
def index():
    return render_template('index.html')

# Background thread that simulates data updates and broadcasts to clients
def simulate_data_updates():
    while True:
        time.sleep(2)  # Simulate data update every 2 seconds
        new_data = {'value': random.randint(1, 100)}  # Generate random data
        print(f"Broadcasting new data: {new_data}")  # Log the update
        socketio.emit('data_update', new_data)  # Broadcast to all clients

# Start the background thread to simulate data updates
thread = threading.Thread(target=simulate_data_updates)
thread.daemon = True  # Ensure the thread will exit when the app closes
thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
