//helper: identify current user
function currentUser() {
  const raw =
    sessionStorage.getItem("userData") || localStorage.getItem("user");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

//interpretation tables (same as matches.js)
const MAP = {
  bedtime: {
    1: "Early Bird (9‑10 PM)",
    2: "Balanced (10‑11 PM)",
    3: "Night Owl (11 PM+)",
  },
  lights: {
    1: "Need complete darkness",
    2: "Prefer dim lighting",
    3: "Comfortable with light",
  },
  clean: { 1: "Very tidy", 2: "Moderately clean", 3: "Relaxed about mess" },
  sharing: {
    1: "Prefer personal items",
    2: "Selective sharing",
    3: "Open to sharing",
  },
  study_location: {
    1: "Library / Outside",
    2: "Mix of locations",
    3: "Room only",
  },
  noise_preference: {
    1: "Complete silence",
    2: "Some background noise",
    3: "Music / Noise okay",
  },
};

//convenience: set <span id="…">
function set(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

//main
document.addEventListener("DOMContentLoaded", async () => {
  const user = currentUser();
  if (!user) {
    window.location.href = "/login";
    return;
  }

  //basic info
  set("user-name", user.username);
  set("user-year", user.classyear ?? "—");
  set("user-email", user.email ?? "—");

  // fetch questionnaire
  let q = null;
  try {
    const res = await fetch(`/api/questionnaire/${user.id}`);
    if (res.ok) q = await res.json();
    else console.warn("No questionnaire on record.");
  } catch (err) {
    console.error("Error loading questionnaire:", err);
  }

  // helper to translate each answer or show dash
  function show(key, spanId = key) {
    if (!q) {
      set(spanId, "—");
      return;
    }
    const raw = q[key];
    if (raw === undefined || raw === null || raw === "") {
      set(spanId, "—");
      return;
    }
    const num = Number(raw);
    set(spanId, MAP[key]?.[num] ?? raw);
  }

  show("bedtime");
  show("lights");
  show("clean");
  show("sharing");
  show("study_location", "study-location");
  show("noise_preference", "noise");
});
