# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    classyear = db.Column(db.Integer, nullable=True)          # NEW
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------------- password helpers ---------------- #
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # -------------- convenience for JSON -------------- #
    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "classyear": self.classyear,
            "created_at": self.created_at.isoformat()
        }

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'),
        unique=True, nullable=False
    )
    answers = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Simple one‑to‑one relationship back to User
    user = db.relationship('User', backref=db.backref(
        'questionnaire', uselist=False, cascade='all,delete-orphan'
    ))
