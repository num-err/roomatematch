import requests

BASE = "http://127.0.0.1:5004"

def register_and_login(username, email, password="pw", classyear="2028"):
    # 1) register
    r = requests.post(
        f"{BASE}/register",
        data={
            "username": username,
            "email": email,
            "password": password,
            "classyear": classyear
        }
    )
    r.raise_for_status()  # fail early if something went wrong

    # 2) login → grab the returned user dict
    r = requests.post(
        f"{BASE}/login",
        data={"username": username, "password": password}
    )
    r.raise_for_status()
    return r.json()["user"]["id"]

def submit_questionnaire(user_id, answers):
    payload = {"user_id": str(user_id), **answers}
    r = requests.post(f"{BASE}/api/questionnaire", data=payload)
    r.raise_for_status()
    return r.json()

def get_match(user_id):
    r = requests.get(f"{BASE}/api/match/{user_id}")
    # if no match, we’ll see a 404
    return r.status_code, r.json()

if __name__ == "__main__":
    # 1) register & login two users
    tosh_id = register_and_login("tosh", "tosh@swarthmore.com")
    mike_id   = register_and_login("mike",   "mike@swarthmore.com")

    # 2) define and submit their questionnaires
    base_answers = dict(
        bedtime="1", bedtime_importance="1",
        lights="2",  lights_importance="2",
        guests="2",  guests_importance="2",
        clean="1",   clean_importance="1",
        mess="1",    mess_importance="1",
        sharing="1", sharing_importance="1",
        study_location="1", study_location_importance="1",
        noise_preference="1", noise_importance="1",
        intended_major="science", major_importance="1",
    )

    # tosh
    print("Submitting Tosh’s questionnaire…")
    print(submit_questionnaire(tosh_id, base_answers))

    # mike: almost the same, just tweak bedtime
    mike_answers = base_answers.copy()
    mike_answers["bedtime"] = "2"
    print("Submitting Mike’s questionnaire…")
    print(submit_questionnaire(mike_id, mike_answers))

    #  3) hit the match endpoint for Tosh
    status, data = get_match(tosh_id)
    print(f"\nGET /api/match/{tosh_id} → HTTP {status}")
    print(data)
