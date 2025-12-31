function startTest(career) {
  window.location.href = "quiz.html?career=" + career;
}

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("careerSearch");
  const careersGrid = document.getElementById("careersGrid");
  const careerCards = document.querySelectorAll(".career-card");
  const searchTestBox = document.getElementById("searchTestBox");
  const searchQuerySpan = document.getElementById("searchQuery");
  const searchTestBtn = document.getElementById("searchTestBtn");

  if (searchInput) {
    searchInput.addEventListener("input", () => {
      const query = searchInput.value.toLowerCase().trim();
      let hasMatch = false;

      careerCards.forEach(card => {
        const career = card.dataset.career.toLowerCase();
        if (career.includes(query)) {
          card.style.display = "block";
          hasMatch = true;
        } else {
          card.style.display = "none";
        }
      });

      if (query.length > 0 && !hasMatch) {
        searchTestBox.style.display = "block";
        searchQuerySpan.textContent = searchInput.value;
        searchTestBtn.onclick = () => startTest(searchInput.value);
      } else {
        searchTestBox.style.display = "none";
      }
    });
  }
});