document.addEventListener("DOMContentLoaded", () => {
    const trainersList  = document.getElementById("trainersList");
    const searchBtn     = document.getElementById("trainerSearchBtn");
    const cityInput     = document.getElementById("trainerCityInput");
    const trainerPlusBtn = document.getElementById("trainerPlusBtn");
    const isLoggedIn = localStorage.getItem("gf_logged_in") === "true";
    const role = localStorage.getItem("gf_role");
    if (!(isLoggedIn && role === "personal_trainer")) {
        if (trainerPlusBtn) trainerPlusBtn.style.display = "none";
    }
    if (trainerPlusBtn) {
        trainerPlusBtn.addEventListener("click", () => {
            window.location.href = "add_trainer.html";
        });
    }
    async function loadTrainersForCity() {
        const city = cityInput.value.trim();
        trainersList.innerHTML = "";
        if (!city) {
            const p = document.createElement("p");
            p.textContent = "Enter a city to see available trainers.";
            trainersList.appendChild(p);
            return;
        }
        try {
            const res = await fetch(`/api/trainers?city=${encodeURIComponent(city)}`);
            const data = await res.json();
            if (!res.ok) {
                const p = document.createElement("p");
                p.textContent = data.error || "Failed to load trainers.";
                trainersList.appendChild(p);
                return;
            }
            const trainersArray = Array.isArray(data) ? data : (data.trainers || []);
            if (!trainersArray.length) {
                const p = document.createElement("p");
                p.textContent = "No trainers found in this city.";
                trainersList.appendChild(p);
                return;
            }
            trainersArray.forEach(tr => {
                const card = document.createElement("div");
                card.className = "gym-card";
                card.dataset.id = tr.id;
                card.innerHTML = `
                    <h3>${tr.personal_trainer_name}</h3>
                    <p>${tr.city}, ${tr.district}, ${tr.country}</p>
                    <p class="gym-small">
                        Experience: ${tr.experience_years} years
                    </p>
                `;
                card.addEventListener("click", () => {
                    window.location.href = `trainer_details.html?id=${tr.id}`;
                });
                trainersList.appendChild(card);
            });
        } catch (err) {
            console.error(err);
            const p = document.createElement("p");
            p.textContent = "Server error while loading trainers.";
            trainersList.appendChild(p);
        }
    }
    searchBtn.addEventListener("click", (e) => {
        e.preventDefault();
        loadTrainersForCity();
    });
    cityInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            loadTrainersForCity();
        }
    });
});
