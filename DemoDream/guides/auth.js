const API_BASE_URL = "http://127.0.0.1:8000/guide";

// Signup Logic
const signupForm = document.getElementById('guideSignupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;
        submitBtn.textContent = "Processing...";

        const data = {
            full_name: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            primary_domain: document.getElementById('primaryDomain').value,
            years_experience: parseInt(document.getElementById('yearsExperience').value),
            current_role: document.getElementById('currentRole').value,
            organization: document.getElementById('currentRole').value, // Split if needed, using same for now
            linkedin_portfolio_url: document.getElementById('linkedinUrl').value,
            bio: document.getElementById('bio').value,
            weekly_availability: document.getElementById('availability').value
        };

        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                alert("Account created! Redirecting to login...");
                window.location.href = "login.html";
            } else {
                alert(result.detail || "Signup failed. Please try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Connection error. Is the backend running?");
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Create Guide Account";
        }
    });
}


// Login Logic moved to the unified login.html
