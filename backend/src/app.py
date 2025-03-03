# app.py
from flask import Flask, request, jsonify
# Import Flask and helper functions for HTTP requests/responses
from config import Config  # Import configuration settings
from models import User, db  # Import User model and SQLAlchemy instance

# Create a new Flask app instance.
app = Flask(__name__)
# Load configuration from the Config class.
app.config.from_object(Config)
# Initialize SQLAlchemy with the Flask app.
db.init_app(app)

# Create all database tables before handling the first request.
@app.before_first_request
def create_tables():
    db.create_all()  # Create tables as defined in the models

# Define the registration route for new users.
@app.route('/register', methods=['POST'])
def register():
    # Parse JSON data from the HTTP request.
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if a user with the same username or email exists.
    if User.query.filter(
        (User.username == username) | (User.email == email)
    ).first():
        return jsonify({
            'error': 'User with that username or email already exists'
        }), 400

    # Create a new user instance with the provided data.
    user = User(username=username, email=email)
    # Set and hash the user's password.
    user.set_password(password)
    # Add the new user to the database session.
    db.session.add(user)
    # Commit the session to save changes.
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# Define the login route for existing users.
@app.route('/login', methods=['POST'])
def login():
    # Parse JSON data from the HTTP request.
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Look up the user by their username.
    user = User.query.filter_by(username=username).first()

    # If user not found or password does not match, return error.
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 400

    # For a real app, generate a session or token here.
    return jsonify({'message': 'Logged in successfully'}), 200

# Run the Flask app in debug mode if this file is executed.
if __name__ == '__main__':
    app.run(debug=True)
