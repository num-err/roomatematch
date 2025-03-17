# app.py
from flask import Flask, request, jsonify  # Import Flask and helpers
from config import Config  # Import configuration settings
from models import User, db  # Import the User model and SQLAlchemy

# Create a new Flask app instance.
app = Flask(__name__)
# Load configuration from Config class.
app.config.from_object(Config)
# Initialize SQLAlchemy with the Flask app.
db.init_app(app)

# Registration route for creating new users.

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get JSON data from the request.
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if a user with this username or email exists.
    if User.query.filter(
        (User.username == username) | (User.email == email)
    ).first():
        return jsonify({
            'error': 'User with that username or email already exists'
        }), 400

    # Create a new user, set the hashed password.
    user = User(username=username, email=email)
    user.set_password(password)
    # Add the new user to the session and commit to the DB.
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# Login route for existing users.
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Parse JSON data from the request.
    username = data.get('username')
    password = data.get('password')

    # Look up the user by username.
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct.
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 400

    # In a real app, we need to generate a token or session.
    return jsonify({'message': 'Logged in successfully'}), 200


@app.route('/get_data' , methods=['GET'])
def get_data():
    data = {'message': 'This is a get request'}
    return jsonify(data)

@app.route('/post_data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        return jsonify({'message': 'This is a POST request', 'data': data}), 201
    else:
         return jsonify({'error': 'Request must be JSON'}), 400
         







# Main block to run the app.
if __name__ == '__main__':
    # Create an application context and initialize the DB.
    with app.app_context():
        db.create_all()  # Create all tables based on models.
    # Run the Flask app in debug mode.
    app.run(debug=True)
