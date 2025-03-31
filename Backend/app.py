from flask import Flask, request, jsonify, render_template
from config import Config
from models import User, db

# Create a new Flask app instance.
app = Flask(__name__, template_folder='../frontend')
app.config.from_object(Config)
db.init_app(app)

# Registration route for creating new users.

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
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
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 400

    return jsonify({'message': 'Logged in successfully'}), 200


@app.route('/')
def index():
    # Fetch data from the database and prepare for rendering
    data = {'message': 'This is a get request'}  # Replace this with your actual data retrieval logic

    # Render the 'index.html' template and pass the retrieved data for rendering
    return render_template('index.html', data=data)


@app.route('/post_data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        return jsonify({'message': 'This is a POST request', 'data': data}), 201
    else:
         return jsonify({'error': 'Request must be JSON'}), 400


if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.run(debug=True)
