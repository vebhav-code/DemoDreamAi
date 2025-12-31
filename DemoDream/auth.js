const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.querySelector(".auth-form[action='signup']"); // I'll need to tag them or use IDs
    const loginForm = document.querySelector(".auth-form[action='login']");

    // Signup logic
    const signupFormEl = document.getElementById("signupForm");
    if (signupFormEl) {
        signupFormEl.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("signup-name").value;
            const email = document.getElementById("signup-email").value;
            const password = document.getElementById("signup-password").value;
            const roleEl = document.getElementById("signup-role");
            const role = roleEl ? roleEl.value : "explorer";

            try {
                const response = await fetch(`${API_BASE_URL}/signup`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name, email, password, role })
                });

                const data = await response.json();
                if (response.ok) {
                    alert("Signup successful! Please login.");
                    window.location.href = "login.html";
                } else {
                    alert(data.detail || "Signup failed");
                }
            } catch (err) {
                console.error("Connection Error:", err);
                alert("Server not reachable. Please make sure the backend is running on port 8000.");
            }
        });
    }

    // Login logic
    const loginFormEl = document.getElementById("loginForm");
    if (loginFormEl) {
        loginFormEl.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("login-email").value;
            const password = document.getElementById("login-password").value;

            try {
                const response = await fetch(`${API_BASE_URL}/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem("userId", data.user.id);
                    localStorage.setItem("userEmail", data.user.email);
                    localStorage.setItem("userName", data.user.name);
                    localStorage.setItem("userRole", data.user.role || 'explorer');

                    alert(`Welcome, ${data.user.name}!`);

                    // Role Check
                    if (data.user.role === 'admin') {
                        window.location.href = "admin_dashboard.html";
                    } else if (data.user.role === 'guide') {
                        window.location.href = "guide_dashboard.html";
                    } else if (data.user.role === 'explorer') {
                        window.location.href = "index.html";
                    } else {
                        window.location.href = "role_selection.html";
                    }
                } else {
                    alert(data.detail || "Login failed");
                }
            } catch (err) {
                console.error("Connection Error:", err);
                alert("Server not reachable. Please make sure the backend is running on port 8000.");
            }
        });
    }
});
