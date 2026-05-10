// ===============================
// 1. PAGE LOAD FADE ANIMATION
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    document.body.style.opacity = 0;

    setTimeout(() => {
        document.body.style.transition = "opacity 0.8s ease";
        document.body.style.opacity = 1;
    }, 100);
});


// ===============================
// 2. BUTTON LOADING STATE
// ===============================
document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", () => {
        const btn = form.querySelector("button");

        if (btn) {
            btn.innerText = "Loading...";
            btn.disabled = true;
        }
    });
});


// ===============================
// 3. MUSIC FACTS ROTATION
// ===============================
const facts = [
    "🎧 Listening to music can reduce stress and anxiety.",
    "🧠 Music improves memory and concentration.",
    "❤️ Your heartbeat syncs with the rhythm of music.",
    "🎵 Music can boost workout performance.",
    "😴 Soft music helps improve sleep quality."
];

let factIndex = 0;

function rotateFacts() {
    const factText = document.getElementById("fact-text");

    if (!factText) return; // safety check

    factText.style.opacity = 0;

    setTimeout(() => {
        factText.innerText = facts[factIndex];
        factText.style.opacity = 1;
        factIndex = (factIndex + 1) % facts.length;
    }, 500);
}

// run every 3 sec
setInterval(rotateFacts, 3000);


// ===============================
// 4. 🔍 SEARCHABLE DROPDOWN (MAIN FIX)
// ===============================

// Get elements safely
const searchInput = document.getElementById("search");
const dropdown = document.getElementById("dropdown");
const hiddenInput = document.getElementById("selectedSong");

// Run only if elements exist (important for multi-page app)
if (searchInput && dropdown && hiddenInput) {

    const items = dropdown.querySelectorAll(".dropdown-item");

    // 👉 Show dropdown when user clicks input
    searchInput.addEventListener("focus", () => {
        dropdown.style.display = "block";
    });

    // 👉 Filter songs while typing
    searchInput.addEventListener("input", function () {
        const value = this.value.toLowerCase();

        items.forEach(item => {
            const text = item.innerText.toLowerCase();

            if (text.includes(value)) {
                item.style.display = "block";
            } else {
                item.style.display = "none";
            }
        });

        dropdown.style.display = "block";
    });

    // 👉 Select song on click
    items.forEach(item => {
        item.addEventListener("click", () => {
            const songName = item.innerText;

            searchInput.value = songName;     // show in input
            hiddenInput.value = songName;     // send to backend
            dropdown.style.display = "none";  // close dropdown
        });
    });

    // 👉 Close dropdown when clicking outside
    document.addEventListener("click", function (e) {
        if (!e.target.closest(".search-box")) {
            dropdown.style.display = "none";
        }
    });
}


// ===============================
// 5. CARD HOVER EFFECT
// ===============================
document.querySelectorAll(".song-card").forEach(card => {
    card.addEventListener("mouseenter", () => {
        card.style.boxShadow = "0 10px 40px rgba(0,0,0,0.6)";
    });

    card.addEventListener("mouseleave", () => {
        card.style.boxShadow = "none";
    });
});