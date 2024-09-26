from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
socketio = SocketIO(app)

# Route to serve the notification page
@app.route('/')
def index():
    return render_template('index.html')

# Function to simulate server-side events that trigger notifications
def generate_notifications():
    notifications = [
        "System Update Available!",
        "New User Registered!",
        "Server Maintenance Scheduled!",
        "You have a new message!",
        "Important Security Alert!"
    ]
    
    while True:
        time.sleep(10)  # Trigger a notification every 10 seconds
        notification = notifications.pop(0)  # Get the next notification
        print(f"Sending notification: {notification}")  # Log the notification
        socketio.emit('new_notification', {'message': notification})  # Emit to all clients
        notifications.append(notification)  # Add it back to the end of the list to cycle through

# Start a background thread that simulates sending notifications
thread = threading.Thread(target=generate_notifications)
thread.daemon = True  # Ensure the thread exits when the app closes
thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
