(function () {
    const publicPages = ["login.html", "signup.html", "career.html", "index.html", "join.html", "howitwork.html"];
    const path = window.location.pathname;
    const currentPage = path.split("/").pop();

    const isPublic = publicPages.includes(currentPage) || currentPage === "" || currentPage === "/";

    const userEmail = localStorage.getItem("userEmail") || localStorage.getItem("guideEmail");
    const userRole = localStorage.getItem("userRole");

    if (isPublic) {
        // If already logged in and trying to access login/signup, redirect to dashboard or home
        if (userEmail && (currentPage === "login.html" || currentPage === "signup.html" || currentPage === "join.html")) {
            if (userRole === 'admin') {
                window.location.href = "admin_dashboard.html";
            } else if (userRole === 'guide') {
                window.location.href = "guide_dashboard.html";
            } else {
                window.location.href = "index.html";
            }
        }
    } else {
        if (!userEmail) {
            console.log("Access denied. Redirecting to login.");
            window.location.href = "login.html";
            return;
        }

        // Admin Protection
        if (currentPage === "admin_dashboard.html" && userRole !== 'admin') {
            window.location.href = "index.html";
        }

        // Search Control: Only explorers see Discovery
        if (currentPage === "discover_guides.html" && userRole === 'guide') {
            window.location.href = "guide_dashboard.html";
        }
    }
})();


