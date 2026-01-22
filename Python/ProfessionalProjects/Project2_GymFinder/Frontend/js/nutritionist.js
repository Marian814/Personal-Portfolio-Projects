document.addEventListener("DOMContentLoaded", () => {
    const listEl       = document.getElementById("nutritionistsList");
    const searchBtn    = document.getElementById("nutritionistSearchBtn");
    const cityInput    = document.getElementById("nutritionistCityInput");
    const plusBtn      = document.getElementById("nutritionistPlusBtn");
    const isLoggedIn       = localStorage.getItem("gf_logged_in") === "true";
    const role               = localStorage.getItem("gf_role");
    if (!(isLoggedIn && role === "nutrition_coach")) {
        if (plusBtn) plusBtn.style.display = "none";
    }
    if (plusBtn) {
        plusBtn.addEventListener("click", () => {
            window.location.href = "add_nutritionist.html";
        });
    }
    async function loadNutritionistsForCity() {
        const city = cityInput.value.trim();
        listEl.innerHTML = "";
        if (!city) {
            const p = document.createElement("p");
            p.textContent = "Enter a city to see available nutritionists.";
            listEl.appendChild(p);
            return;
        }
        try {
            const res = await fetch(`/api/nutritionists?city=${encodeURIComponent(city)}`);
            const data = await res.json();
            if (!res.ok) {
                const p = document.createElement("p");
                p.textContent = data.error || "Failed to load nutritionists.";
                listEl.appendChild(p);
                return;
            }
            const arr = Array.isArray(data) ? data : (data.nutritionists || []);
            if (!arr.length) {
                const p = document.createElement("p");
                p.textContent = "No nutritionists found in this city.";
                listEl.appendChild(p);
                return;
            }
            arr.forEach(nutr => {
                const card = document.createElement("div");
                card.className = "gym-card";
                card.dataset.id = nutr.id;
                card.innerHTML = `
                    <h3>${nutr.nutritionist_name}</h3>
                    <p>${nutr.city}, ${nutr.district}, ${nutr.country}</p>
                    <p class="gym-small">
                        Experience: ${nutr.experience_years} years
                    </p>
                `;
                card.addEventListener("click", () => {
                    window.location.href = `nutritionist_details.html?id=${nutr.id}`;
                });
                listEl.appendChild(card);
            });
        } catch (err) {
            console.error(err);
            const p = document.createElement("p");
            p.textContent = "Server error while loading nutritionists.";
            listEl.appendChild(p);
        }
    }
    searchBtn.addEventListener("click", (e) => {
        e.preventDefault();
        loadNutritionistsForCity();
    });
    cityInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            loadNutritionistsForCity();
        }
    });
});
