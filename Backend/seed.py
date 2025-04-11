# seed.py
from app import app, db, User

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        user1 = User(username='tosh', email='tosh@swarthmore.com', classyear=2026)
        user1.set_password('tosh123')

        user2 = User(username='mike', email='mike@example.com', classyear=2025)
        user2.set_password('mike456')

        db.session.add_all([user1, user2])
        db.session.commit()
        print("Dummy data added successfully!")

if __name__ == "__main__":
    seed_data()
