# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    classyear = db.Column(db.String(10), nullable=True)          # NEW
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
   # __tablename__ = 'questionnaires'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'),
        unique=True, nullable=False
    )

    bedtime = db.Column(db.String(30), nullable=False)  
    bedtime_importance = db.Column(db.Integer, nullable=False)  
    lights = db.Column(db.Integer, nullable=False)  
    lights_importance = db.Column(db.Integer, nullable=False)  
    guests = db.Column(db.Integer, nullable=False) 
    guests_importance = db.Column(db.Integer, nullable=False)  

    # Cleanliness and Organization Section
    clean = db.Column(db.Integer, nullable=False)  
    clean_importance = db.Column(db.Integer, nullable=False)  
    mess = db.Column(db.Integer, nullable=False)  
    mess_importance = db.Column(db.Integer, nullable=False)  
    sharing = db.Column(db.Integer, nullable=False)  
    sharing_imp = db.Column(db.Integer, nullable=False)  

    # Study Habits Section
    study_location = db.Column(db.String(30), nullable=False)  
    study_location_importance = db.Column(db.String(20), nullable=False) 
    noise_preference = db.Column(db.String(30), nullable=False)  
    noise_importance = db.Column(db.String(20), nullable=False)  
    intended_major = db.Column(db.String(30), nullable=False)  
    major_importance = db.Column(db.String(20), nullable=False) 

    
    # Social Preferences Section (Last Section)
    personality_type = db.Column(db.String(30), nullable=False)  # Introverted, Extroverted, etc.
    personality_importance = db.Column(db.Integer, nullable=False)
    going_out_frequency = db.Column(db.String(30), nullable=False)  # How often they go out
    going_out_importance = db.Column(db.Integer, nullable=False)
    people_over_preference = db.Column(db.String(30), nullable=False)  # How often they have people over
    people_over_importance = db.Column(db.Integer, nullable=False)
    
     
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref(
        'questionnaire', uselist=False, cascade='all,delete-orphan'
    ))

    #def __repr__(self):
        #return f'<Questionnaire {self.id}>'

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            
            # Sleep Preferences
            'bedtime': self.bedtime,
            'bedtime_importance': self.bedtime_importance,
            'lights': self.lights,
            'lights_importance': self.lights_importance,
            'guests': self.guests,
            'guests_importance': self.guests_importance,
            
            # Cleanliness and Organization
            'clean': self.clean,
            'clean_importance': self.clean_importance,
            'mess': self.mess,
            'mess_importance': self.mess_importance,
            'sharing': self.sharing,
            'sharing_imp': self.sharing_imp,
            
            # Study Habits
            'study_location': self.study_location,
            'study_location_importance': self.study_location_importance,
            'noise_preference': self.noise_preference,
            'noise_importance': self.noise_importance,
            'intended_major': self.intended_major,
            'major_importance': self.major_importance,
            
            'social_preference': self.social_preference,
            'social_importance': self.social_importance,

            # Social Preferences (Last Section)
            'personality_type': self.personality_type,
            'personality_importance': self.personality_importance,
            'going_out_frequency': self.going_out_frequency,
            'going_out_importance': self.going_out_importance,
            'people_over_preference': self.people_over_preference,
            'people_over_importance': self.people_over_importance,
            'roommate_going_out_preference': self.roommate_going_out_preference,
            
            'timestamp': self.timestamp.isoformat()
        }

class Message(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    sender_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    receiver_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    content = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

    #comment merge conglict