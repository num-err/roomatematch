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
  // Map database field keys → human‑readable labels
  const labels = {
    bedtime: "Bedtime",
    lights: "Lights tolerance",
    guests: "Overnight guests",
    clean: "Cleaning frequency",
    mess: "Mess tolerance",
    sharing: "Sharing items",
    study_location: "Study location",
    noise_preference: "Noise while studying",
    intended_major: "Intended major",
  };

  return `
    <ul class="questionnaire-list">
      ${Object.entries(labels)
        .map(
          ([key, label]) =>
            `<li><strong>${label}:</strong> ${q[key] ?? "—"}</li>`,
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

    <button class="view-q-btn">View their questionnaire</button>
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
