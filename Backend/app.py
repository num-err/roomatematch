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
#from seed import seed_data

#  Flask setup
BASE_DIR      = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRONTEND_DIR  = os.path.join(BASE_DIR, 'frontend')

app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,   # where Jinja2 looks for *.html
    static_folder=FRONTEND_DIR,     # where Flask serves CSS/JS/img
    static_url_path='/'             # "LoginPage/styles.css", etc.
)
print(f"[Flask] FRONTEND_DIR = {FRONTEND_DIR}")

app.config.from_object(Config)
db.init_app(app)

#  Helper static serving
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

#  Simple matching Algo
def _distance(a1: dict, a2: dict) -> int:
    """
    Sum of absolute differences for answers that look like numbers.
    For non‑numeric answers: 0 if same, 1 if different i.e major and bedtime
    """
    score = 0
    #Comparing 2 sets person 1 and person 2
    for key in (set(a1) & set(a2)):
        v1, v2 = a1[key], a2[key]
        try:
            #For numerical answers
            score += abs(int(v1) - int(v2))
        except ValueError:
            #For text/matching answers
            score += 0 if v1 == v2 else 1
    return score

def _best_match_for(user_id: int):
    """
    Return the User instance that is *closest* to user_id,
    or None if no other questionnaires exist.
    """
    # Get current user's questionnaire
    me_q = Questionnaire.query.filter_by(user_id=user_id).first()
    if not me_q:
        return None
    # Get all OTHER users' questionnaires
    others = (
        Questionnaire.query
        .filter(Questionnaire.user_id != user_id)
        .all()
    )
    if not others:
        return None

    # find min distance
    best_row   = min(others, key=lambda q: _distance(me_q.answers, q.answers))
    # Get corresponding User
    best_user  = User.query.get(best_row.user_id)
    return best_user

#  Front‑end routes
@app.route('/')
def index():
    return _serve_frontend_file('LoginPage/register.html')

@app.route('/register')
def serve_register():
    return _serve_frontend_file('LoginPage/register.html')

@app.route('/login')
def serve_login():
    return _serve_frontend_file('LoginPage/index.html')

@app.route('/questionnaire')
def serve_questionnaire():
    return _serve_frontend_file('UserInterface/questionaire.html')

#  Authentication API
@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form['username']
        classyear = request.form['classyear']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter(
            (User.username == username) | (User.email == email)
        ).first():
            return jsonify({'error': 'User with that username or email already exists'})

        user = User(username=username, email=email, classyear=classyear)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': 'User registered successfully',
            'redirect': '/login'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'})

        return jsonify({
            'message': 'Logged in successfully',
            'user': user.as_dict(),
            'redirect': '/questionnaire'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)})

#  Questionnaire section routes
@app.route('/questionnaire/section1', methods=['GET'])
def questionnaire_section1():
    return _serve_frontend_file('UserInterface/questionaire.html')

@app.route('/questionnaire/section2', methods=['GET'])
def questionnaire_section2():
    return _serve_frontend_file('UserInterface/questionaire.html')

@app.route('/questionnaire/section3', methods=['GET'])
def questionnaire_section3():
    return _serve_frontend_file('UserInterface/questionaire.html')

@app.route('/questionnaire/section4', methods=['GET'])
def questionnaire_section4():
    return _serve_frontend_file('UserInterface/questionaire.html')

# questionnaire submission endpoint
@app.route('/api/questionnaire', methods=['POST'])
def submit_questionnaire():
    try:

        print(request.form)

        # Get user_id from form data
        user_id = request.form['user_id']
        print("user_id")


        # Get all questionnaire answers from form data
        questionnaire = Questionnaire(
            user_id=user_id,
            bedtime=request.form['bedtime'],
            bedtime_importance=request.form['bedtime_importance'],
            lights=request.form['lights'],
            lights_importance=request.form['lights_importance'],
            guests=request.form['guests'],
            guests_importance=request.form['guests_importance'],

            clean = request.form['clean'],
            clean_importance= request.form['clean_importance'],
            mess= request.form['mess'],
            mess_importance= request.form['mess_importance'],
            sharing= request.form['sharing'],
            sharing_importance= request.form['sharing_importance'],

            study_location = request.form['study_location'],
            study_location_importance = request.form['study_location_importance'],
            noise_preference = request.form['noise_preference'],
            noise_importance = request.form['noise_importance'],
            intended_major = request.form['intended_major'],
            major_importance = request.form['major_importance'],


        )

        print("questionnaire")

        # Check if user already has a questionnaire
        existing_questionnaire = Questionnaire.query.filter_by(user_id=user_id).first()

        print("existing_questionnaire")
        print(existing_questionnaire)

        if existing_questionnaire:
            # Update existing questionnaire
            for key, value in request.form.items():
                if hasattr(existing_questionnaire, key):
                    setattr(existing_questionnaire, key, value)
            db.session.commit()
            return jsonify({'message': 'Questionnaire updated successfully'}), 200
        else:
            # Create new questionnaire
            db.session.add(questionnaire)
            db.session.commit()
            return jsonify({'message': 'Questionnaire submitted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#  Messaging endpoints
@app.route('/sendMessage', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id   = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content     = data.get('content')

    if not sender_id or not receiver_id or not content:
        return jsonify({'error': 'Missing fields'}), 400

    message = Message(
        sender_id = sender_id,
        receiver_id = receiver_id,
        content = content
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully'}), 201


#  Simple GET user_id
@app.route('/api/match/<int:user_id>', methods=['GET'])
def api_match(user_id: int):
    best = _best_match_for(user_id)
    if best is None:
        return jsonify({'message': 'No match found'})
    return jsonify(best.as_dict())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004)

"""@app.route('/getMessage', methods=['GET'])
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

#  Dummy test route
@app.route('/post_data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        return jsonify({'message': 'This is a POST request', 'data': data}), 201
    return jsonify({'error': 'Request must be JSON'}), 400"""





#Scraped for now

# #  Questionnaire & matching API
# def _questionnaire_distance(a1: dict, a2: dict) -> int:
#     """
#     Simple numeric distance: sum(|answer_i - answer_j|).
#     Non‑numeric answers count 1 if different, 0 if same.
#     """
#     keys = set(a1) & set(a2)
#     score = 0
#     for k in keys:
#         try:
#             score += abs(int(a1[k]) - int(a2[k]))
#         except Exception:
#             score += 0 if a1[k] == a2[k] else 1
#     return score


# def _build_preferences():
#     """
#     Pull every completed questionnaire and convert to
#     Gale–Shapley preference lists.
#     Returns: (proposers, receivers, prop_prefs, recv_prefs)
#     or None if we don't have both sides yet.
#     """
#     q_rows = Questionnaire.query.all()
#     if len(q_rows) < 2:
#         return None  # need at least two people

#     answers = {q.user_id: q.answers for q in q_rows}
#     users   = list(answers.keys())

#     # Distance matrix
#     dist = {u: {} for u in users}
#     for u in users:
#         for v in users:
#             if u == v:
#                 continue
#             dist[u][v] = _questionnaire_distance(answers[u], answers[v])

#     # Arbitrary split: even‑id users propose, odd‑id users receive
#     proposers  = [u for u in users if u % 2 == 0]
#     receivers  = [u for u in users if u % 2 == 1]
#     if not proposers or not receivers:
#         return None

#     prop_prefs = {p: sorted(receivers, key=lambda r: dist[p][r]) for p in proposers}
#     recv_prefs = {r: sorted(proposers, key=lambda p: dist[r][p]) for r in receivers}
#     return proposers, receivers, prop_prefs, recv_prefs


# def _run_matching_for(user_id: int):
#     """
#     Execute Gale–Shapley and return the matched User (or None)
#     for the given user_id.
#     """
#     prefs = _build_preferences()
#     if prefs is None:
#         return None  # not enough data yet

#     proposers, receivers, prop_prefs, recv_prefs = prefs
#     matches = stable_matching(proposers, receivers, prop_prefs, recv_prefs)

#     # matches is {proposer -> receiver}
#     partner_id = None
#     if user_id in matches:                 # user is a proposer
#         partner_id = matches[user_id]
#     else:                                  # user may be a receiver
#         for p, r in matches.items():
#             if r == user_id:
#                 partner_id = p
#                 break

#     return User.query.get(partner_id) if partner_id else None


# @app.route('/api/questionnaire', methods=['POST'])
# def submit_questionnaire():
#     """
#     Expected JSON:
#     {
#         "user_id": <int>,
#         "answers": { "bedtime": "2", "bedtime-importance": "3", ... }
#     }
#     """
#     data      = request.get_json(silent=True) or {}
#     user_id   = data.get('user_id')
#     answers   = data.get('answers')

#     if not user_id or not answers:
#         return jsonify({'error': 'user_id and answers required'}), 400

#     # Upsert questionnaire
#     q = Questionnaire.query.filter_by(user_id=user_id).first()
#     if q:
#         q.answers   = answers
#         q.timestamp = datetime.utcnow()
#     else:
#         q = Questionnaire(user_id=user_id, answers=answers)
#         db.session.add(q)

#     db.session.commit()

#     # Try to find a match immediately
#     partner = _run_matching_for(user_id)
#     if partner:
#         return jsonify({
#             'message': 'Questionnaire saved',
#             'match': partner.as_dict()
#         }), 200

#     return jsonify({
#         'message': 'Questionnaire saved – waiting for more students'
#     }), 200
