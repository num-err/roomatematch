# Roommate Match

A web app that pairs college students with compatible roommates based on the habits that usually cause roommate conflict: sleep schedule, cleanliness, guests, noise, and study habits.

Built as a team project with Lola, Mathew Agani, and Mugdha.

**Stack:** Python · Flask · SQLAlchemy · SQLite · HTML/CSS · JavaScript

---

## How it works

1. **Sign up** with a username, email, password, and class year. Passwords are stored as salted hashes (Werkzeug).
2. **Answer the questionnaire** — four sections covering:
   - Sleep: bedtime, lights on/off
   - Social: guests, sharing belongings
   - Cleanliness: tidiness, tolerance for mess
   - Study: where you study, noise preference, intended major

   Each answer also has an **importance** rating, so you can say what you care about most.
3. **Get matched.** The app compares your answers with every other user's and returns the closest one. Numeric answers are scored by how far apart they are; text answers (like major or bedtime) score 0 if they match and 1 if they don't. The lowest total distance is the best match.
4. **View your profile** with your match and edit your info or answers anytime.

`gale_shapley.py` contains a stable-matching (Gale–Shapley) implementation for pairing everyone at once so that no two people would both rather be with each other than with their assigned roommate. It isn't wired into the app yet.

## API

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/register` | Create an account |
| `POST` | `/login` | Log in |
| `POST` | `/api/questionnaire` | Submit questionnaire answers |
| `GET` | `/api/questionnaire/<user_id>` | Get a user's answers |
| `GET` | `/api/match/<user_id>` | Get the closest match for a user |
| `POST` | `/api/update-profile` | Update username, email, or class year |
| `POST` | `/sendMessage` | Send a message to another user |

## Running locally

```bash
git clone https://github.com/num-err/roomatematch.git
cd roomatematch/Backend
python3 -m venv venv && source venv/bin/activate
pip install flask flask-sqlalchemy
python seed.py          # optional: sample users
python app.py
```

Open `http://127.0.0.1:5004`.

## Project layout

```
Backend/
  app.py               Flask routes and matching logic
  models.py            User, Questionnaire, and Message models
  gale_shapley.py      stable-matching algorithm
  seed.py              sample data
  test_live_matching.py  end-to-end script against a running server
frontend/
  LoginPage/           sign up and log in
  UserInterface/       questionnaire, profile, matches, messages
  js/                  page logic
```

## Next steps

- Use the importance ratings to weight the match score
- Run Gale–Shapley across all users for stable, campus-wide pairing
- Finish in-app messaging
