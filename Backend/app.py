# app.py
import os
from datetime import datetime
from flask import (
    Flask, request, jsonify, render_template,
    send_from_directory, abort, redirect, url_for
)
from config import Config
from models import User, db, Questionnaire
from gale_shapley import stable_matching

#  Flask setup
BASE_DIR      = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRONTEND_DIR  = os.path.join(BASE_DIR, 'frontend')

app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,   # where Jinja2 looks for *.html
    static_folder=FRONTEND_DIR,     # where Flask serves CSS/JS/img
    static_url_path='/'             # “/LoginPage/styles.css”, etc.
)
print(f"[Flask] FRONTEND_DIR = {FRONTEND_DIR}")

app.config.from_object(Config)
db.init_app(app)


#  Helper for ad‑hoc static serving
def _serve_frontend_file(relative_path: str):
    """
    Serve a file from the frontend directory if it exists,
    otherwise return 404.
    """
    abs_path = os.path.join(FRONTEND_DIR, relative_path)
    print(f"[Flask] Trying to serve {abs_path}")
    if os.path.exists(abs_path):
        print(f"[Flask] ➜  sending {abs_path}")
        return send_from_directory(FRONTEND_DIR, relative_path)
    print(f"[Flask] ✖  {abs_path} not found")
    abort(404)


#  Front‑end routes
@app.route('/')
def index():
    # Redirect root to the login page
    return redirect(url_for('loginpage_root'))


@app.route('/LoginPage/')
def loginpage_root():
    return render_template('LoginPage/index.html')


# Fallbacks for any other assets under /frontend
@app.route('/UserInterface/<path:filename>')
def userinterface_files(filename):
    return _serve_frontend_file(os.path.join('UserInterface', filename))


@app.route('/<path:filename>')
def any_frontend_file(filename):
    return _serve_frontend_file(filename)


#  Authentication API
@app.route('/register', methods=['POST'])
def register():
    data       = request.get_json()
    username   = data.get('username')
    email      = data.get('email')
    password   = data.get('password')
    classyear  = data.get('classyear')

    if User.query.filter(
        (User.username == username) | (User.email == email)
    ).first():
        return jsonify({'error': 'User with that username or email already exists'}), 400

    user = User(username=username, email=email, classyear=classyear)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data     = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 400

    return jsonify({'message': 'Logged in successfully', 'user': user.as_dict()}), 200


#  Questionnaire & matching API
def _questionnaire_distance(a1: dict, a2: dict) -> int:
    """
    Simple numeric distance: sum(|answer_i - answer_j|).
    Non‑numeric answers count 1 if different, 0 if same.
    """
    keys = set(a1) & set(a2)
    score = 0
    for k in keys:
        try:
            score += abs(int(a1[k]) - int(a2[k]))
        except Exception:
            score += 0 if a1[k] == a2[k] else 1
    return score


def _build_preferences():
    """
    Pull every completed questionnaire and convert to
    Gale–Shapley preference lists.
    Returns: (proposers, receivers, prop_prefs, recv_prefs)
    or None if we don't have both sides yet.
    """
    q_rows = Questionnaire.query.all()
    if len(q_rows) < 2:
        return None  # need at least two people

    answers = {q.user_id: q.answers for q in q_rows}
    users   = list(answers.keys())

    # Distance matrix
    dist = {u: {} for u in users}
    for u in users:
        for v in users:
            if u == v:
                continue
            dist[u][v] = _questionnaire_distance(answers[u], answers[v])

    # Arbitrary split: even‑id users propose, odd‑id users receive
    proposers  = [u for u in users if u % 2 == 0]
    receivers  = [u for u in users if u % 2 == 1]
    if not proposers or not receivers:
        return None

    prop_prefs = {p: sorted(receivers, key=lambda r: dist[p][r]) for p in proposers}
    recv_prefs = {r: sorted(proposers, key=lambda p: dist[r][p]) for r in receivers}
    return proposers, receivers, prop_prefs, recv_prefs


def _run_matching_for(user_id: int):
    """
    Execute Gale–Shapley and return the matched User (or None)
    for the given user_id.
    """
    prefs = _build_preferences()
    if prefs is None:
        return None  # not enough data yet

    proposers, receivers, prop_prefs, recv_prefs = prefs
    matches = stable_matching(proposers, receivers, prop_prefs, recv_prefs)

    # matches is {proposer -> receiver}
    partner_id = None
    if user_id in matches:                 # user is a proposer
        partner_id = matches[user_id]
    else:                                  # user may be a receiver
        for p, r in matches.items():
            if r == user_id:
                partner_id = p
                break

    return User.query.get(partner_id) if partner_id else None


@app.route('/api/questionnaire', methods=['POST'])
def submit_questionnaire():
    """
    Expected JSON:
    {
        "user_id": <int>,
        "answers": { "bedtime": "2", "bedtime-importance": "3", ... }
    }
    """
    data      = request.get_json(silent=True) or {}
    user_id   = data.get('user_id')
    answers   = data.get('answers')

    if not user_id or not answers:
        return jsonify({'error': 'user_id and answers required'}), 400

    # Upsert questionnaire
    q = Questionnaire.query.filter_by(user_id=user_id).first()
    if q:
        q.answers   = answers
        q.timestamp = datetime.utcnow()
    else:
        q = Questionnaire(user_id=user_id, answers=answers)
        db.session.add(q)

    db.session.commit()

    # Try to find a match immediately
    partner = _run_matching_for(user_id)
    if partner:
        return jsonify({
            'message': 'Questionnaire saved',
            'match': partner.as_dict()
        }), 200

    return jsonify({
        'message': 'Questionnaire saved – waiting for more students'
    }), 200



@app.route('/post_data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        return jsonify({'message': 'This is a POST request', 'data': data}), 201
    return jsonify({'error': 'Request must be JSON'}), 400



# This is an endpoint set for sending a message 
@app.route('/messages' , methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    if not sender_id or not receiver_id or not content:
        return jsonify({'error': 'Missing fields'}), 400

    message = Message(
        sender_id = sender_id
        receiver_id = receiver_id
        content = content
    ) 

    db.session.add(message)
    db.session.commit()

    return jsonify({'message' : 'Message sent succesfully'}) , 201

    #comment merge conflict 

#This is a route to get all the messages shared betweeen two students
# It is going to be relevant if we decide to go with chat instead of just a notification message

@app.route('/messages', methods=['GET'])
def get_messages():
    user1 = request.args.get('user1', type=int)
    user2 = request.args.get('user2', type=int)

    if not user1 or not user2:
        return jsonify({'error': 'Both user IDs are required'}), 400

    messages = Message.query.filter(
        ((Message.sender_id == user1) & (Message.receiver_id == user2)) |
        ((Message.sender_id == user2) & (Message.receiver_id == user1))
    ).order_by(Message.timestamp.asc()).all()

    return jsonify([{
        'sender_id': m.sender_id,
        'receiver_id': m.receiver_id,
        'content': m.content,
        'timestamp': m.timestamp.isoformat()
    } for m in messages]), 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
