# app.py
import os
from flask import (
    Flask, request, jsonify, render_template, send_from_directory, abort
)
from config import Config
from models import User, db

# Flask setup
app = Flask(__name__, template_folder='../frontend')
app.config.from_object(Config)
db.init_app(app)

# Absolute path to the frontend directory (LoginPage, UserInterface, etc.)
FRONTEND_DIR = os.path.abspath(os.path.join(app.root_path, '..', 'frontend'))
print(f"[Flask] FRONTEND_DIR = {FRONTEND_DIR}")

# Helper for safe static‑file serving
def _serve_frontend_file(relative_path: str):
    """
    Serve a file from the frontend directory if it exists,
    otherwise return 404.
    """
    abs_path = os.path.join(FRONTEND_DIR, relative_path)
    print(f"[Flask] Trying to serve {abs_path}")  # Debug info
    if os.path.exists(abs_path):
        print(f"[Flask] ➜  sending {abs_path}")
        return send_from_directory(FRONTEND_DIR, relative_path)
    print(f"[Flask] ✖  {abs_path} not found")
    abort(404)


# Static routes
@app.route('/LoginPage/')
def loginpage_root():
    # /LoginPage/  ->  .../frontend/LoginPage/index.html
    return _serve_frontend_file(os.path.join('LoginPage', 'index.html'))

@app.route('/UserInterface/<path:filename>')
def userinterface_files(filename):
    return _serve_frontend_file(os.path.join('UserInterface', filename))

@app.route('/<path:filename>')
def any_frontend_file(filename):
    """
    Generic catch‑all for anything else inside /frontend
    e.g. /LoginPage/styles.css
    """
    return _serve_frontend_file(filename)

# Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username   = data.get('username')
    email      = data.get('email')
    password   = data.get('password')
    classyear  = data.get('classyear')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'User with that username or email already exists'}), 400

    user = User(username=username, email=email, classyear=classyear)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 400

    return jsonify({'message': 'Logged in successfully', 'user': user.as_dict()}), 200


# Demo root
@app.route('/')
def index():
    # just to show the server is running
    return render_template('index.html', data={'message': 'This is a GET request'})


# POST demo
@app.route('/post_data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        return jsonify({'message': 'This is a POST request', 'data': data}), 201
    return jsonify({'error': 'Request must be JSON'}), 400

# Main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
