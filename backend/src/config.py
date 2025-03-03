# config.py
import os  # Import OS module for file and path operations

# Get the absolute path of the directory of this file.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Define the SQLite database URI using the BASE_DIR.
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    )
    # Disable SQLAlchemy modification tracking.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Secret key
    SECRET_KEY = 'your-secret-key'
