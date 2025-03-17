# seed.py

from app import app, db, User

def seed_data():
    with app.app_context():
        #Drops all tables
        db.drop_all()
        #Creates all tables
        db.create_all()

        # Create a few dummy users
        user1 = User(username='tosh', email='tosh@swarthmore.com')
        user1.set_password('tosh123')
        user2 = User(username='mike', email='mike@example.com')
        user2.set_password('mike456')

        # Add them to the session and commit
        db.session.add_all([user1, user2])
        db.session.commit()

        print("Dummy data added successfully!")

if __name__ == "__main__":
    seed_data()
