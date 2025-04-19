//returns the user's id
function getCurrentUserId() {
  let raw = sessionStorage.getItem("userData") || localStorage.getItem("user");
  if (!raw) return null;
  try {
    return JSON.parse(raw).id;
  } catch (err) {
    console.error("Could not parse user data:", err);
    return null;
  }
}

//makes data legible
function renderQuestionnaire(q) {
  // Map database field keys → human‑readable labels and interpretations
  const interpretations = {
    bedtime: {
      label: "Bedtime",
      values: {
        1: "Early Bird (9-10 PM)",
        2: "Balanced (10-11 PM)",
        3: "Night Owl (11 PM+)"
      }
    },
    lights: {
      label: "Lights tolerance",
      values: {
        1: "Need complete darkness",
        2: "Prefer dim lighting",
        3: "Comfortable with light"
      }
    },
    guests: {
      label: "Overnight guests",
      values: {
        1: "Rarely",
        2: "Occasionally",
        3: "Frequently"
      }
    },
    clean: {
      label: "Cleaning frequency",
      values: {
        1: "Very tidy",
        2: "Moderately clean",
        3: "Relaxed about mess"
      }
    },
    mess: {
      label: "Mess tolerance",
      values: {
        1: "Very low",
        2: "Moderate",
        3: "High"
      }
    },
    sharing: {
      label: "Sharing items",
      values: {
        1: "Prefer personal items",
        2: "Selective sharing",
        3: "Open to sharing"
      }
    },
    study_location: {
      label: "Study location",
      values: {
        1: "Library/Outside",
        2: "Mix of locations",
        3: "Room only"
      }
    },
    noise_preference: {
      label: "Noise while studying",
      values: {
        1: "Complete silence",
        2: "Some background noise",
        3: "Music/Noise okay"
      }
    },
    intended_major: {
      label: "Intended major",
      values: {
        "engineering": "Engineering",
        "business": "Business",
        "arts": "Arts",
        "sciences": "Sciences",
        "other": "Other"
      }
    }
  };

  return `
    <ul class="questionnaire-list">
      ${Object.entries(interpretations)
        .map(
          ([key, data]) =>
            `<li><strong>${data.label}:</strong> <span>${data.values[q[key]] ?? "—"}</span></li>`,
        )
        .join("")}
    </ul>
  `;
}

// visable card
function buildMatchCard(matchUser) {
  const card = document.createElement("div");
  card.className = "match-card";

  card.innerHTML = `
    <div class="match-header">
      <h2 class="match-name">${matchUser.username}</h2>
      <p class="match-year">Class of ${matchUser.classyear ?? ""}</p>
    </div>

    <button class="view-q-btn">View their Profile</button>
    <div class="q-box" style="display:none; margin-top:1rem;"></div>
  `;

  const btn = card.querySelector(".view-q-btn");
  const box = card.querySelector(".q-box");
  let loaded = false;

  btn.addEventListener("click", async () => {
    if (!loaded) {
      try {
        const r = await fetch(`/api/questionnaire/${matchUser.id}`);
        if (r.ok) {
          const q = await r.json();
          box.innerHTML = renderQuestionnaire(q);
        } else {
          box.innerHTML = "<p>(Could not load questionnaire.)</p>";
        }
      } catch (err) {
        console.error("Error loading questionnaire:", err);
        box.innerHTML = "<p>(Error loading questionnaire.)</p>";
      }
      loaded = true;
    }
    // toggle visibility
    box.style.display = box.style.display === "none" ? "block" : "none";
  });

  return card;
}

//main
document.addEventListener("DOMContentLoaded", async () => {
  const userId = getCurrentUserId();
  if (!userId) {
    console.error("No user ID found. Please log in.");
    // optional: window.location.href = "/login";
    return;
  }

  let response;
  try {
    response = await fetch(`/api/match/${userId}`);
  } catch (err) {
    console.error("Network error while fetching match:", err);
    return;
  }

  if (!response.ok) {
    // 404 means no match yet → leave placeholders
    return;
  }

  const matchUser = await response.json(); // {id, username, ...}

  // Replace only the first placeholder card
  const list = document.getElementById("matches-list");
  const placeholder = list.querySelector(".match-card.placeholder");
  if (!placeholder) {
    console.warn("No placeholder found to replace.");
    return;
  }

  const newCard = buildMatchCard(matchUser);
  list.replaceChild(newCard, placeholder);
});
