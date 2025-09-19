from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import logging

# --- App Initialization ---
# Setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-secret-key-that-is-secure' 
# In a real app, use an environment variable for this

# Initialize SocketIO with gevent and allow all origins
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

# --- Standard HTTP Routes ---
@app.route('/')
def index():
    """A simple health check endpoint to verify the API is running."""
    return jsonify({"status": "ok", "message": "Remote click WebSocket API is running."})

# --- WebSocket Event Handlers ---
@socketio.on('connect')
def handle_connect():
    """Logs when a client connects to the WebSocket."""
    logging.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Logs when a client disconnects."""
    logging.info('Client disconnected')

@app.route('/click', methods=['POST'])
def handle_click_http():
    """
    Handles a click event from the host PC via a standard POST request.
    It then broadcasts this event to all connected WebSocket clients.
    """
    logging.info('Click event received via HTTP POST')
    # Broadcast to all clients
    socketio.emit('click_event', {'coords': None}) 
    return jsonify({"status": "ok", "message": "Click event broadcasted."})

# --- Main Execution Block ---
# This block allows us to run the app directly with 'python main.py'
# The built-in gevent server is the most reliable way to run flask-socketio
if __name__ == '__main__':
    print("Starting Flask-SocketIO server directly...")
    socketio.run(app, host='0.0.0.0', port=5000)

