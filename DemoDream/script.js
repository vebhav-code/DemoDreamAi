// ============================
// Navigation Update (Login/Profile)
// ============================
document.addEventListener("DOMContentLoaded", () => {
  const nav = document.querySelector("nav");
  const userEmail = localStorage.getItem("userEmail");

  if (userEmail && nav) {
    const loginLink = Array.from(nav.querySelectorAll("a")).find(a => a.innerText.includes("Login"));

    // 1. Hide original Login link if it exists
    if (loginLink) {
      loginLink.style.display = "none";
    }

    // 2. Create Dropdown Container (only if not already present)
    if (!document.querySelector(".profile-dropdown-container")) {
      const container = document.createElement("div");
      container.className = "profile-dropdown-container";

      const userName = localStorage.getItem("userName") || "User";
      const userInitial = userName.charAt(0).toUpperCase();

      container.innerHTML = `
        <button class="profile-trigger" id="profileTrigger">
            <div class="avatar-circle">${userInitial}</div>
            <span class="dropdown-arrow">▼</span>
        </button>
        <div class="profile-menu" id="profileMenu">
            <div class="menu-header">
                <div class="menu-avatar-large">${userInitial}</div>
                <div class="menu-user-info">
                    <h4 id="menuUserName">${userName}</h4>
                    <p id="menuUserEmail">${userEmail}</p>
                </div>
            </div>
            <div class="stats-row">
                <div class="stat-box stat-purple">💎 6770</div>
                <div class="stat-box stat-blue">⭐ 6830</div>
            </div>
            <ul class="menu-list">
                ${localStorage.getItem("userRole") === 'guide' ? `
                <li class="menu-item" onclick="window.location.href='guide_dashboard.html'">
                    <div class="menu-item-icon">📊</div> Guide Dashboard
                </li>` : ''}
                <li class="menu-item" onclick="window.location.href='profile.html'">
                    <div class="menu-item-icon">👤</div> My Profile
                </li>
                ${localStorage.getItem("userRole") === 'explorer' ? `
                <li class="menu-item" onclick="window.location.href='discover_guides.html'">
                    <div class="menu-item-icon">🔍</div> Discover Guides
                </li>` : ''}
                <li class="menu-item" onclick="window.location.href='my_careers.html'">
                    <div class="menu-item-icon">📚</div> My Careers
                </li>
                <li class="menu-item" onclick="window.location.href='dream_project.html'">
                    <div class="menu-item-icon">🚀</div> MyDreamProject
                </li>
                <li class="menu-item" onclick="window.location.href='live_dream.html'">
                    <div class="menu-item-icon">✨</div> Live Dream
                </li>
                <li class="menu-item">
                    <div class="menu-item-icon">🔒</div> Change Password
                </li>
                <li class="menu-item">
                    <div class="menu-item-icon">❓</div> FAQ
                </li>
                <li class="menu-item" id="darkModeItem">
                    <div class="menu-item-icon">🌙</div> Dark Mode
                </li>
                <li class="menu-item logout" id="logoutBtn">
                     <div class="menu-item-icon">↪️</div> Sign Out
                </li>
            </ul>
        </div>
      `;

      // 3. Append to Nav
      nav.appendChild(container);

      // 4. Toggle Logic
      const trigger = container.querySelector("#profileTrigger");
      const menu = container.querySelector("#profileMenu");

      trigger.addEventListener("click", (e) => {
        e.stopPropagation();
        container.classList.toggle("active");
      });

      // Close when clicking outside
      document.addEventListener("click", (e) => {
        if (!container.contains(e.target)) {
          container.classList.remove("active");
        }
      });

      // 5. Logout Logic
      const logoutBtn = container.querySelector("#logoutBtn");
      logoutBtn.addEventListener("click", () => {
        localStorage.clear(); // Clear all to be safe and remove unwanted clutter
        window.location.href = "login.html";
      });

      // 6. Dark Mode Logic (Inside Dropdown)
      const darkModeItem = document.getElementById("darkModeItem");
      if (darkModeItem) {
        darkModeItem.addEventListener("click", (e) => {
          e.stopPropagation(); // Prevent closing dropdown
          const isDark = document.body.classList.toggle("dark-mode");
          localStorage.setItem("darkMode", isDark ? "enabled" : "disabled");
        });
      }
    }
  }

  // Global Dark Mode Check on Load
  if (localStorage.getItem("darkMode") === "enabled") {
    document.body.classList.add("dark-mode");
  }
});

// ============================
// Handle "Get Started" button
// ============================
document.addEventListener("DOMContentLoaded", () => {
  const getStartedBtn = document.querySelector(".cta-btn");
  if (getStartedBtn) {
    getStartedBtn.addEventListener("click", function (e) {
      e.preventDefault();
      window.open("howitworks.html", "_blank", "noopener,noreferrer");
    });
  }
});

// ============================
// Tagline Rotator (Homepage)
// ============================
document.addEventListener("DOMContentLoaded", () => {
  const taglines = document.querySelectorAll(".tagline");
  if (taglines.length > 0) {
    let index = 0;

    function showNextTagline() {
      taglines.forEach((tag, i) => {
        tag.classList.remove("active");
        if (i === index) {
          tag.classList.add("active");
        }
      });
      index = (index + 1) % taglines.length;
    }

    // Show first tagline immediately
    showNextTagline();

    // Rotate every 2.5 seconds
    setInterval(showNextTagline, 2500);
  }
});

// ============================
// Dark Mode Toggle (Index only, applies to all pages)
// ============================

// ============================
// Future: Form handling
// (login / signup validation, etc.)
// ============================
// You can add your backend/DB connection later.
// For now, these forms just exist in login.html

// ============================
// Career Selection + Description + Test Navigation
// ============================

document.addEventListener("DOMContentLoaded", () => {
  const careerItems = document.querySelectorAll(".career-item");
  const searchInput = document.getElementById("careerSearch");
  const detailsBox = document.getElementById("careerDetails");
  const titleEl = document.getElementById("careerTitle");
  const descEl = document.getElementById("careerDescription");
  const startTestBtn = document.getElementById("startTestBtn");

  const descriptions = {
    "Doctor": "Doctors diagnose illnesses, prescribe treatments and improve patient health.",
    "Engineer": "Engineers design and build machines, structures, and technologies.",
    "Lawyer": "Lawyers interpret laws, represent clients, and solve legal disputes.",
    "Teacher": "Teachers educate students and help develop their academic foundations.",
    "Pilot": "Pilots operate aircraft, navigate routes and ensure passenger safety.",
    "Scientist": "Scientists research, experiment, and discover solutions to world problems.",
    "Artist": "Artists create visual or performance works expressing ideas and emotion."
  };

  // Handle search filtering
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      const query = searchInput.value.toLowerCase();

      careerItems.forEach(item => {
        const name = item.innerText.toLowerCase();
        item.style.display = name.includes(query) ? "block" : "none";
      });
    });
  }

  // Handle clicking a career
  careerItems.forEach(item => {
    item.addEventListener("click", () => {
      const career = item.dataset.career;

      titleEl.innerText = career;
      descEl.innerText = descriptions[career] || "No description available.";

      // Show the description box
      detailsBox.style.display = "block";

      // Set action for test button
      startTestBtn.onclick = () => {
        window.location.href = `quiz.html?career=${career}`;
      };
    });
  });
});
