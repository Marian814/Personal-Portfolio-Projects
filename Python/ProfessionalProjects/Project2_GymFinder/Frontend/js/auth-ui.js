function logoutAndRedirect() {
    localStorage.removeItem("gf_logged_in");
    localStorage.removeItem("gf_username");
    localStorage.removeItem("gf_role");
    window.location.href = "index.html";
}

document.addEventListener("DOMContentLoaded", () => {
    const loginHeaderBtn = document.getElementById("loginHeaderBtn");
    const signupHeaderBtn = document.getElementById("signupHeaderBtn");
    const menuLoginLink = document.getElementById("menuLoginLink");
    const menuSignupLink = document.getElementById("menuSignupLink");
    const menuGym = document.getElementById("menuGymLink");
    const menuTrainer = document.getElementById("menuTrainerLink");
    const menuNutrition = document.getElementById("menuNutritionLink");
    const isLoggedIn = localStorage.getItem("gf_logged_in") === "true";
    const role = localStorage.getItem("gf_role");
    if (isLoggedIn) {
        if (loginHeaderBtn) {
            loginHeaderBtn.querySelector("span").textContent = "Log Out";
            loginHeaderBtn.onclick = logoutAndRedirect;
        }
        if (signupHeaderBtn) {
            signupHeaderBtn.style.display = "none";
        }
        if (menuLoginLink) {
            menuLoginLink.textContent = "Log Out";
            menuLoginLink.href = "#";
            menuLoginLink.onclick = (e) => {
                e.preventDefault();
                logoutAndRedirect();
            };
        }
        if (menuSignupLink) {
            menuSignupLink.style.display = "none";
        }
        if (menuGym) menuGym.style.display = "block";
        if (menuTrainer) menuTrainer.style.display = "block";
        if (menuNutrition) menuNutrition.style.display = "block";
    } else {
        if (loginHeaderBtn) {
            loginHeaderBtn.querySelector("span").textContent = "Log In";
            loginHeaderBtn.onclick = () => window.location.href = "login.html";
        }
        if (signupHeaderBtn) {
            signupHeaderBtn.style.display = "flex";
            signupHeaderBtn.onclick = () => window.location.href = "signup.html";
        }
        if (menuLoginLink) {
            menuLoginLink.textContent = "Log In";
            menuLoginLink.href = "login.html";
            menuLoginLink.onclick = null;
        }
        if (menuSignupLink) {
            menuSignupLink.style.display = "block";
        }
        if (menuGym) menuGym.style.display = "none";
        if (menuTrainer) menuTrainer.style.display = "none";
        if (menuNutrition) menuNutrition.style.display = "none";
    }
    const plusBtn = document.getElementById("plusBtn");
    if (plusBtn) {
        const currentPage = window.location.pathname.split("/").pop();
        let shouldShow = false;
        if (isLoggedIn) {
            if (role === "gym_owner" && currentPage === "gym.html") {
                shouldShow = true;
            } else if (role === "personal_trainer" && currentPage === "trainer.html") {
                shouldShow = true;
            } else if (role === "nutrition_coach" && currentPage === "nutritionist.html") {
                shouldShow = true;
            }
        }
        plusBtn.style.display = shouldShow ? "inline-block" : "none";
    }
});
