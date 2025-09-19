from flask import Flask, jsonify
from threading import Lock

# Initialize the Flask app
app = Flask(__name__)

# A simple in-memory data store to track clicks.
# We use a dictionary for the counter and a thread lock for safety.
click_data = {"count": 0}
lock = Lock()

@app.route('/click', methods=['POST'])
def register_click():
    """
    Endpoint for the HOST computer to call.
    Increments the click counter.
    """
    global click_data
    with lock:
        click_data["count"] += 1
    print(f"Click registered. Total pending clicks: {click_data['count']}")
    return jsonify(status="success", message="click registered"), 200

@app.route('/check-click', methods=['GET'])
def check_for_click():
    """
    Endpoint for the CLIENT computer to call.
    Checks if there are pending clicks and consumes one if available.
    """
    global click_data
    perform_click = False
    with lock:
        if click_data["count"] > 0:
            click_data["count"] -= 1
            perform_click = True
            print(f"Click signal sent to client. Remaining clicks: {click_data['count']}")
    
    return jsonify(click=perform_click)

@app.route('/status', methods=['GET'])
def status():
    """A simple health-check endpoint."""
    return jsonify(status="ok", pending_clicks=click_data["count"])

if __name__ == '__main__':
    # Runs the app on port 5000, accessible from any IP address within the container.
    app.run(host='0.0.0.0', port=5000)
