from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import logging

# --- Application Setup ---
app = Flask(__name__)
# The secret key is needed for session management, although we don't use sessions heavily.
app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_changed'
# We now use gevent as the async mode for better Windows compatibility
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- HTTP Endpoints ---

@app.route("/")
def index():
    """
    A simple root endpoint to confirm the API is running via HTTP.
    """
    return jsonify({"status": "ok", "message": "Remote Click WebSocket API is running."})

@app.route('/click', methods=['POST'])
def record_click():
    """
    Receives a standard HTTP click event from the host.
    This is the only part of the old system we're keeping.
    """
    data = request.json if request.is_json else {}
    coords = data.get('coords')

    # Broadcast the 'click_event' to all connected WebSocket clients.
    # The payload includes the coordinates if they were sent.
    socketio.emit('click_event', {'coords': coords})

    if coords:
        logging.info(f"Click event received with coords {coords}, broadcasting to clients.")
    else:
        logging.info("Click event received without coords, broadcasting to clients.")

    return jsonify({"status": "ok", "message": "Click event broadcasted."})

# --- WebSocket Event Handlers ---

@socketio.on('connect')
def handle_connect():
    """
    This function is called when a new client connects via WebSocket.
    """
    logging.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """
    This function is called when a client disconnects.
    """
    logging.info(f"Client disconnected: {request.sid}")

# --- Main Execution ---
# The entry point is now managed by gunicorn via the Dockerfile.
if __name__ == '__main__':
    # This will run a development server.
    socketio.run(app, host='0.0.0.0', port=5000)

