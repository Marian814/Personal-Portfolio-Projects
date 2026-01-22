document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addNutritionistForm");
    const messageEl = document.getElementById("nutritionistMessage");
    const nameInput        = document.getElementById("nutritionistName");
    const countryInput     = document.getElementById("country");
    const districtInput    = document.getElementById("district");
    const cityInput        = document.getElementById("city");
    const experienceInput  = document.getElementById("experience");
    const descriptionInput = document.getElementById("description");
    const isLoggedIn = localStorage.getItem("gf_logged_in") === "true";
    const role       = localStorage.getItem("gf_role");
    const userId     = localStorage.getItem("gf_user_id");
    const username   = localStorage.getItem("gf_username");
    if (!isLoggedIn || role !== "nutrition_coach" || !userId) {
        if (messageEl) {
            messageEl.style.color = "red";
            messageEl.textContent = "You must be logged in as a Nutrition Coach to access this page.";
        }
        setTimeout(() => {
            window.location.href = "login.html";
        }, 2000);
        return;
    }
    if (username && nameInput && !nameInput.value) {
        nameInput.value = username;
    }
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        messageEl.textContent = "";
        const nutritionist_name = nameInput.value.trim();
        const country           = countryInput.value.trim();
        const district          = districtInput.value.trim();
        const city              = cityInput.value.trim();
        const experienceStr     = experienceInput.value.trim();
        const description       = descriptionInput.value.trim();
        if (!nutritionist_name || !country || !district || !city || !experienceStr) {
            messageEl.style.color = "red";
            messageEl.textContent = "All fields except description are required.";
            return;
        }
        const experience_years = parseInt(experienceStr, 10);
        if (Number.isNaN(experience_years) || experience_years < 0) {
            messageEl.style.color = "red";
            messageEl.textContent = "Experience must be a non-negative number.";
            return;
        }
        const payload = {
            nutritionist_name,
            country,
            district,
            city,
            experience_years,
            description,
            nutritionist_id: userId
        };
        try {
            const res = await fetch("/api/nutritionists", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (!res.ok) {
                messageEl.style.color = "red";
                messageEl.textContent = data.error || "Failed to create nutritionist profile.";
                return;
            }
            messageEl.style.color = "lightgreen";
            messageEl.textContent = "Nutritionist profile created successfully.";
            if (data.id) {
                setTimeout(() => {
                    window.location.href = `nutritionist_details.html?id=${data.id}`;
                }, 1200);
            } else {
                setTimeout(() => {
                    window.location.href = "nutritionist.html";
                }, 1200);
            }
        } catch (err) {
            console.error(err);
            messageEl.style.color = "red";
            messageEl.textContent = "Server error.";
        }
    });
});
