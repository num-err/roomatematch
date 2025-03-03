# models.py
from flask_sqlalchemy import SQLAlchemy  # ORM for database operations
from datetime import datetime  # For recording timestamps
from werkzeug.security import (  # Import functions to hash passwords
    generate_password_hash, check_password_hash
)

# Initialize SQLAlchemy instance.
db = SQLAlchemy()

class User(db.Model):
    # User model represents a user in the database.

    # Primary key: unique ID for each user.
    id = db.Column(db.Integer, primary_key=True)

    # Username: must be unique and not null.
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Email: must be unique and not null.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Store the hashed password (not the plain text).
    password_hash = db.Column(db.String(128), nullable=False)

    # Timestamp when the user account was created.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        # Hash the given password and store it.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Compare provided password with the stored hash.
        return check_password_hash(self.password_hash, password)
