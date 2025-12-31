document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("loader");
    const quizArea = document.getElementById("questionsArea");
    const cardContainer = document.getElementById("questionCards");

    const pageTitle = document.getElementById("quizTitle");
    const careerBadge = document.getElementById("careerBadge");
    const difficultyBadge = document.getElementById("difficultyBadge");

    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const submitBtn = document.getElementById("submitQuiz");

    const resultPanel = document.getElementById("resultPanel");
    const resultScore = document.getElementById("resultScore");

    let questions = [];

    const params = new URLSearchParams(window.location.search);
    const career = params.get("career") || "General";

    if (pageTitle) pageTitle.textContent = `${career} Test`;
    if (careerBadge) careerBadge.textContent = career;

    // Hide pagination controls as we are showing all questions
    if (prevBtn) prevBtn.style.display = "none";
    if (nextBtn) nextBtn.style.display = "none";

    // Hide progress bar initially or permanently as it's a single list
    const progressRow = document.querySelector(".progress-row");
    if (progressRow) progressRow.style.display = "none";

    async function loadQuestions() {
        try {
            const response = await fetch("http://127.0.0.1:8000/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    field: career,
                    difficulty: "basic"
                })
            });

            const data = await response.json();
            questions = data.questions;

            if (!questions || questions.length === 0) {
                loader.innerHTML = "<h3>AI returned no questions. Try again.</h3>";
                return;
            }

            loader.style.display = "none";
            quizArea.style.display = "block";

            renderAllQuestions();

        } catch (err) {
            console.error(err);
            loader.innerHTML = "<h3>Backend not reachable (8000)</h3>";
        }
    }

    function renderAllQuestions() {
        cardContainer.innerHTML = ""; // Clear existing

        questions.forEach((q, index) => {
            const optionsHtml = (q.options || []).map(opt => {
                const trimmedOpt = opt.trim();
                const optionLetter = trimmedOpt.match(/^[A-D]/i) ? trimmedOpt.charAt(0).toUpperCase() : trimmedOpt;

                return `
                    <label class="option" style="display:block; margin: 8px 0;">
                        <input type="radio" 
                            name="q${q.id}" 
                            value="${optionLetter}">
                        ${trimmedOpt}
                    </label>
                `;
            }).join("");

            const questionCard = document.createElement("div");
            questionCard.className = "question-card";
            questionCard.style.marginBottom = "30px"; // Spacing between cards
            questionCard.innerHTML = `
                <h2>${index + 1}. ${q.question}</h2>
                <div class="options-container">
                    ${optionsHtml}
                </div>
            `;
            cardContainer.appendChild(questionCard);
        });

        // Ensure submit button is visible
        submitBtn.style.display = "block";
    }

    if (submitBtn) {
        submitBtn.addEventListener("click", async () => {
            let correct = 0;
            let answeredCount = 0;

            questions.forEach(q => {
                const selected = document.querySelector(`input[name="q${q.id}"]:checked`);
                if (selected) {
                    answeredCount++;
                    if (selected.value === q.correct_answer) {
                        correct++;
                    }
                }
            });

            if (answeredCount < questions.length) {
                if (!confirm(`You have answered ${answeredCount} out of ${questions.length} questions. Do you want to submit anyway?`)) {
                    return;
                }
            }

            let percent = Math.round((correct / questions.length) * 100);

            quizArea.style.display = "none";
            resultPanel.style.display = "block";
            resultScore.textContent = `${percent}%`;

            // Eligibility Logic
            const resultDetail = document.getElementById("resultDetail");
            let eligibility = "";
            let badgeClass = "";
            let feedback = "";

            if (percent >= 80) {
                eligibility = "Highly Eligible";
                badgeClass = "eligibility-high";
                feedback = `Excellent! You have a profound understanding of ${career}. You are ready for the next level.`;
            } else if (percent >= 50) {
                eligibility = "Eligible";
                badgeClass = "eligibility-mid";
                feedback = `Good job! You have the foundational knowledge for ${career}, but some areas need sharpening.`;
            } else {
                eligibility = "Needs More Preparation";
                badgeClass = "eligibility-low";
                feedback = `Consistency is key. You should study more about the fundamentals of ${career} and retake the test.`;
            }

            resultDetail.innerHTML = `
                <div class="eligibility-badge ${badgeClass}">${eligibility}</div>
                <p>${feedback}</p>
            `;

            const userEmail = localStorage.getItem("userEmail");
            if (userEmail) {
                try {
                    await fetch("http://127.0.0.1:8000/save-result", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            user_email: userEmail,
                            career: career,
                            score: percent,
                            difficulty: "basic"
                        })
                    });
                } catch (err) {
                    console.error("Failed to save performance:", err);
                }
            }

            // Redirect to Results Page
            window.location.href = `result.html?career=${encodeURIComponent(career)}&score=${percent}`;
        });
    }

    loadQuestions();
});
