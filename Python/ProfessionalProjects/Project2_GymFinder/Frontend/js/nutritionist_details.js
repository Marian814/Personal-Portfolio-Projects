document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("nutritionistDetails");
    const subsSlider = document.getElementById("subsSlider");
    const addSubBtn = document.getElementById("addSubBtn");
    const addSubForm = document.getElementById("addSubForm");
    const subPriceInput = document.getElementById("subPriceInput");
    const subBenefitsInput = document.getElementById("subBenefitsInput");
    const saveSubBtn = document.getElementById("saveSubBtn");
    const subMessage = document.getElementById("subMessage");
    const prevSubBtn = document.getElementById("prevSubBtn");
    const nextSubBtn = document.getElementById("nextSubBtn");
    let subsSlides = [];
    let currentSubIndex = 0;
    const params = new URLSearchParams(window.location.search);
    const nutrId = params.get("id");
    if (!nutrId) {
        container.innerHTML = "<p>Missing nutritionist id.</p>";
        return;
    }
    const isLoggedIn = localStorage.getItem("gf_logged_in") === "true";
    const role = localStorage.getItem("gf_role");
    const userId = localStorage.getItem("gf_user_id");
    let isOwnerOfNutritionist = false;
    try {
        const res = await fetch(`/api/nutritionists/${nutrId}`);
        const data = await res.json();
        if (!res.ok) {
            container.innerHTML = `<p>${data.error || "Nutritionist not found."}</p>`;
            return;
        }
        const nutr = data;
        if (isLoggedIn && role === "nutrition_coach" && userId && nutr.nutritionist_id) {
            isOwnerOfNutritionist = parseInt(userId, 10) === nutr.nutritionist_id;
        }
        container.innerHTML = `
            <div class="gym-details-card">
                <div class="details-header">
                    ${isOwnerOfNutritionist ? `
                        <button id="deleteNutritionistBtn"
                                class="delete-btn"
                                title="Delete nutritionist profile">✕</button>
                    ` : ""}
                    <h1>${nutr.nutritionist_name}</h1>
                </div>
                <p class="gym-location">
                    ${nutr.city}, ${nutr.district}, ${nutr.country}
                </p>
                <p class="gym-owner">
                    Experience: <strong>${nutr.experience_years} years</strong>
                </p>
                <p class="gym-description">
                    ${nutr.description || "No description provided."}
                </p>
            </div>
        `;
        if (!isOwnerOfNutritionist) {
            if (addSubBtn) addSubBtn.style.display = "none";
            if (addSubForm) addSubForm.style.display = "none";
        }
        if (isOwnerOfNutritionist) {
            const deleteBtn = document.getElementById("deleteNutritionistBtn");
            if (deleteBtn) {
                deleteBtn.addEventListener("click", async () => {
                    if (!confirm("Delete this nutritionist profile?")) return;
                    try {
                        const delRes = await fetch(`/api/nutritionists/${nutrId}`, {
                            method: "DELETE",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ user_id: userId })
                        });
                        const delData = await delRes.json();
                        if (!delRes.ok) {
                            alert(delData.error || "Failed to delete nutritionist.");
                            return;
                        }
                        alert("Nutritionist profile deleted.");
                        window.location.href = "nutritionist.html";
                    } catch (err) {
                        console.error(err);
                        alert("Server error.");
                    }
                });
            }
        }
    } catch (err) {
        console.error(err);
        container.innerHTML = "<p>Server error loading nutritionist details.</p>";
        return;
    }
    async function loadSubscriptions() {
        subsSlider.innerHTML = "";
        subsSlides = [];
        currentSubIndex = 0;
        try {
            const res = await fetch(`/api/nutritionists/${nutrId}/subscriptions`);
            const data = await res.json();
            if (!res.ok) {
                subsSlider.innerHTML = "<p>Failed to load subscriptions.</p>";
                return;
            }
            const subsArray = Array.isArray(data) ? data : (data.subscriptions || []);
            if (!subsArray.length) {
                subsSlider.innerHTML = "<p>No subscriptions yet for this nutritionist.</p>";
                if (prevSubBtn) prevSubBtn.style.display = "none";
                if (nextSubBtn) nextSubBtn.style.display = "none";
                return;
            }
            subsArray.forEach((sub, index) => {
                const slide = document.createElement("div");
                slide.className = "subscription-slide";
                if (index === 0) slide.classList.add("active");
                slide.innerHTML = `
                    <div class="subscription-title">Plan #${index + 1}</div>
                    <div class="subscription-benefits">
                        ${sub.benefits || "No benefits specified."}
                    </div>
                    <div class="subscription-price-row">
                        <div class="subscription-price">${sub.price} RON</div>
                        <button class="buy-btn"
                                data-sub-id="${sub.id}"
                                data-price="${sub.price}">
                            Buy
                        </button>
                    </div>
                `;
                subsSlider.appendChild(slide);
            });
            document.querySelectorAll(".buy-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    const subId = btn.dataset.subId;
                    const price = btn.dataset.price;
                    window.location.href = `payment.html?sub=${subId}&price=${price}`;
                });
            });
            subsSlides = Array.from(subsSlider.querySelectorAll(".subscription-slide"));
            updateSubsSliderUI();
        } catch (err) {
            console.error(err);
            subsSlider.innerHTML = "<p>Server error loading subscriptions.</p>";
        }
    }
    function updateSubsSliderUI() {
        if (!subsSlides.length) {
            if (prevSubBtn) prevSubBtn.style.display = "none";
            if (nextSubBtn) nextSubBtn.style.display = "none";
            return;
        }
        subsSlides.forEach((slide, idx) => {
            slide.classList.toggle("active", idx === currentSubIndex);
        });
        const showNav = subsSlides.length > 1;
        if (prevSubBtn) prevSubBtn.style.display = showNav ? "flex" : "none";
        if (nextSubBtn) nextSubBtn.style.display = showNav ? "flex" : "none";
    }
    if (prevSubBtn) {
        prevSubBtn.addEventListener("click", () => {
            if (!subsSlides.length) return;
            currentSubIndex = (currentSubIndex - 1 + subsSlides.length) % subsSlides.length;
            updateSubsSliderUI();
        });
    }
    if (nextSubBtn) {
        nextSubBtn.addEventListener("click", () => {
            if (!subsSlides.length) return;
            currentSubIndex = (currentSubIndex + 1) % subsSlides.length;
            updateSubsSliderUI();
        });
    }
    if (isOwnerOfNutritionist) {
        if (addSubBtn) {
            addSubBtn.addEventListener("click", () => {
                if (addSubForm.style.display === "flex") {
                    addSubForm.style.display = "none";
                    subMessage.textContent = "";
                    subPriceInput.value = "";
                    subBenefitsInput.value = "";
                } else {
                    addSubForm.style.display = "flex";
                }
            });
        }
        if (saveSubBtn) {
            saveSubBtn.addEventListener("click", async () => {
                const price = subPriceInput.value.trim();
                const benefits = subBenefitsInput.value.trim();
                if (!price) {
                    subMessage.style.color = "red";
                    subMessage.textContent = "Price is required.";
                    return;
                }
                if (!userId) {
                    subMessage.style.color = "red";
                    subMessage.textContent = "You must be logged in.";
                    return;
                }
                try {
                    const res = await fetch(`/api/nutritionists/${nutrId}/subscriptions`, {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            price: price,
                            benefits: benefits,
                            user_id: userId
                        })
                    });
                    const data = await res.json();
                    if (!res.ok) {
                        subMessage.style.color = "red";
                        subMessage.textContent = data.error || "Failed to add subscription.";
                        return;
                    }
                    subMessage.style.color = "lightgreen";
                    subMessage.textContent = "Subscription added successfully.";
                    await loadSubscriptions();
                    subPriceInput.value = "";
                    subBenefitsInput.value = "";
                } catch (err) {
                    console.error(err);
                    subMessage.style.color = "red";
                    subMessage.textContent = "Server error.";
                }
            });
        }
    }
    loadSubscriptions();
});
