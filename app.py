from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Sample data storage (in-memory)
users = {}
mood_data = {}
resources = {
    1: {"title": "Understanding Anxiety", "content": "Article on managing anxiety."},
    2: {"title": "Meditation Guide", "content": "Guide to start meditation."}
}

@app.route('/')
def index():
    return render_template('index.html')

# User Registration
@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if email in users:
        return jsonify({"message": "User already exists."}), 400

    users[email] = {
        "name": name,
        "password": password,
        "mood_history": []
    }

    return jsonify({"message": "User registered successfully!"}), 201

# User Login
@app.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users.get(email)
    if user and user['password'] == password:
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid email or password."}), 401

# User Profile
@app.route('/users/profile', methods=['GET'])
def get_user_profile():
    email = request.args.get('email')
    user = users.get(email)
    if user:
        return jsonify({
            "name": user['name'],
            "mood_history": user['mood_history']
        }), 200
    return jsonify({"message": "User not found."}), 404

# Mood Tracking
@app.route('/mood', methods=['POST'])
def record_mood():
    data = request.json
    email = data.get('email')
    mood = data.get('mood')

    user = users.get(email)
    if user:
        user['mood_history'].append(mood)
        return jsonify({"message": "Mood recorded successfully!"}), 200
    return jsonify({"message": "User not found."}), 404

@app.route('/mood/history', methods=['GET'])
def get_mood_history():
    email = request.args.get('email')
    user = users.get(email)
    if user:
        return jsonify({"mood_history": user['mood_history']}), 200
    return jsonify({"message": "User not found."}), 404

# Mental Health Resources
@app.route('/resources', methods=['GET'])
def get_resources():
    return jsonify(resources), 200

@app.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = resources.get(resource_id)
    if resource:
        return jsonify(resource), 200
    return jsonify({"message": "Resource not found."}), 404

# Counselor Support
@app.route('/counselor/connect', methods=['POST'])
def connect_counselor():
    data = request.json
    email = data.get('email')
    session_type = data.get('session_type')  # 'chat' or 'video'
    if email in users:
        return jsonify({"message": f"Connected to a counselor for a {session_type} session."}), 200
    return jsonify({"message": "User not found."}), 404

# Crisis Support
@app.route('/crisis/help', methods=['POST'])
def trigger_crisis_support():
    data = request.json
    email = data.get('email')
    if email in users:
        # Here you could implement logic to alert crisis teams
        return jsonify({"message": "Crisis support triggered."}), 200
    return jsonify({"message": "User not found."}), 404

@app.route('/crisis/hotlines', methods=['GET'])
def get_crisis_hotlines():
    # Example hotlines
    hotlines = {
        "USA": "1-800-273-TALK (1-800-273-8255)",
        "India": "022 2754 6669"
    }
    return jsonify(hotlines), 200

# Notifications and Reminders
@app.route('/notifications/reminders', methods=['POST'])
def set_reminder():
    data = request.json
    email = data.get('email')
    reminder = data.get('reminder')

    if email in users:
        # Store reminders in a way appropriate for your app (not implemented here)
        return jsonify({"message": "Reminder set successfully!"}), 200
    return jsonify({"message": "User not found."}), 404

@app.route('/notifications/schedule', methods=['GET'])
def get_reminders():
    email = request.args.get('email')
    if email in users:
        # Here you would retrieve reminders (not implemented here)
        return jsonify({"message": "Retrieve user reminders."}), 200
    return jsonify({"message": "User not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
