document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("gymDetails");
    const photosSlider = document.getElementById("gymPhotosSlider");
    const addPhotoBtn = document.getElementById("addPhotoBtn");
    const addPhotoForm = document.getElementById("addPhotoForm");
    const photoUrlInput = document.getElementById("photoUrlInput");
    const savePhotoBtn = document.getElementById("savePhotoBtn");
    const photoMessage = document.getElementById("photoMessage");
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
    const gymId = params.get("id");
    if (!gymId) {
        container.innerHTML = "<p>Missing gym id.</p>";
        return;
    }
    const isLoggedIn = localStorage.getItem("gf_logged_in") === "true";
    const role = localStorage.getItem("gf_role");
    const userId = localStorage.getItem("gf_user_id");
    let isOwnerOfGym = false;
    try {
        const res = await fetch(`/api/gyms/${gymId}`);
        const data = await res.json();
        if (!res.ok) {
            container.innerHTML = `<p>${data.error || "Gym not found."}</p>`;
            return;
        }
        const gym = data;
        if (isLoggedIn && role === "gym_owner" && userId && gym.owner_id) {
            isOwnerOfGym = parseInt(userId, 10) === gym.owner_id;
        }
        container.innerHTML = `
            <div class="gym-details-card">
                <div class="details-header">
                    ${isOwnerOfGym ? `
                        <button id="deleteGymBtn"
                                class="delete-btn"
                                title="Delete gym">✕</button>
                    ` : ""}
                    <h1>${gym.gym_name}</h1>
                </div>
                <p class="gym-location">
                    ${gym.street} ${gym.street_number}, ${gym.city}, ${gym.district}, ${gym.country}
                </p>
                <p class="gym-owner">
                    Owner: <strong>${gym.gym_owner_name}</strong>
                </p>
                <p class="gym-description">
                    ${gym.description || "No description provided."}
                </p>
                <p class="gym-size">
                    Size: ${gym.size_m2 ? gym.size_m2 + " m²" : "N/A"}
                </p>
                <div class="gym-features">
                    <span class="${gym.has_locker_room ? "feat-on" : "feat-off"}">Locker Room</span>
                    <span class="${gym.has_boxing ? "feat-on" : "feat-off"}">Boxing</span>
                    <span class="${gym.has_sauna ? "feat-on" : "feat-off"}">Sauna</span>
                    <span class="${gym.has_pool ? "feat-on" : "feat-off"}">Pool</span>
                </div>
                ${gym.google_maps_link ? `
                    <p class="gym-maps">
                        <a href="${gym.google_maps_link}" target="_blank">
                            View on Google Maps
                        </a>
                    </p>
                ` : ""}
            </div>
        `;
        if (!isOwnerOfGym) {
            if (addPhotoBtn) addPhotoBtn.style.display = "none";
            if (addPhotoForm) addPhotoForm.style.display = "none";
            if (addSubBtn) addSubBtn.style.display = "none";
            if (addSubForm) addSubForm.style.display = "none";
        }
        if (isOwnerOfGym) {
            const deleteBtn = document.getElementById("deleteGymBtn");
            if (deleteBtn) {
                deleteBtn.addEventListener("click", async () => {
                    const ok = confirm("Are you sure you want to delete this gym?");
                    if (!ok) return;
                    try {
                        const delRes = await fetch(`/api/gyms/${gymId}`, {
                            method: "DELETE",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ user_id: userId })
                        });
                        const delData = await delRes.json();
                        if (!delRes.ok) {
                            alert(delData.error || "Failed to delete gym.");
                            return;
                        }
                        alert("Gym deleted.");
                        window.location.href = "gym.html";
                    } catch (err) {
                        console.error(err);
                        alert("Server error.");
                    }
                });
            }
        }
    } catch (err) {
        console.error(err);
        container.innerHTML = "<p>Server error loading gym details.</p>";
        return;
    }
    async function loadPhotos() {
        photosSlider.innerHTML = "";
        try {
            const res = await fetch(`/api/gyms/${gymId}/photos`);
            const data = await res.json();
            if (!res.ok) {
                photosSlider.innerHTML = "<p>Failed to load photos.</p>";
                return;
            }
            const photosArray = Array.isArray(data) ? data : (data.photos || []);
            if (!photosArray.length) {
                photosSlider.innerHTML = "<p>No photos yet for this gym.</p>";
                return;
            }
            photosArray.forEach((photo, index) => {
                const src = photo.photo_url;
                console.log("PHOTO SRC:", src);
                const slide = document.createElement("div");
                slide.className = "gym-photo-slide";
                if (index === 0) slide.classList.add("active");
                const img = document.createElement("img");
                img.src = src;
                img.alt = "Gym photo";
                slide.appendChild(img);
                photosSlider.appendChild(slide);
            });
            setupPhotoSlider();
        } catch (err) {
            console.error(err);
            photosSlider.innerHTML = "<p>Server error loading photos.</p>";
        }
    }
    function setupPhotoSlider() {
        const slides = photosSlider.querySelectorAll(".gym-photo-slide");
        if (slides.length <= 1) return;
        let current = 0;
        setInterval(() => {
            slides[current].classList.remove("active");
            current = (current + 1) % slides.length;
            slides[current].classList.add("active");
        }, 4000);
    }
    async function loadSubscriptions() {
        subsSlider.innerHTML = "";
        subsSlides = [];
        currentSubIndex = 0;
        try {
            const res = await fetch(`/api/gyms/${gymId}/subscriptions`);
            const data = await res.json();
            if (!res.ok) {
                subsSlider.innerHTML = "<p>Failed to load subscriptions.</p>";
                return;
            }
            const subsArray = Array.isArray(data) ? data : (data.subscriptions || []);
            if (!subsArray.length) {
                subsSlider.innerHTML = "<p>No subscriptions yet for this gym.</p>";
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
    if (isLoggedIn && role === "gym_owner" && isOwnerOfGym) {
        if (addPhotoBtn) {
            addPhotoBtn.addEventListener("click", () => {
                if (addPhotoForm.style.display === "flex") {
                    addPhotoForm.style.display = "none";
                    photoMessage.textContent = "";
                    photoUrlInput.value = "";
                } else {
                    addPhotoForm.style.display = "flex";
                }
            });
        }
        if (savePhotoBtn) {
            savePhotoBtn.addEventListener("click", async () => {
                const urlRaw = photoUrlInput.value.trim();
                const url = urlRaw;
                if (!url) {
                    photoMessage.style.color = "red";
                    photoMessage.textContent = "Please paste an image link.";
                    return;
                }
                if (!userId) {
                    photoMessage.style.color = "red";
                    photoMessage.textContent = "You must be logged in.";
                    return;
                }
                try {
                    const res = await fetch(`/api/gyms/${gymId}/photos`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ photo_url: url, user_id: userId })
                    });
                    const data = await res.json();
                    if (!res.ok) {
                        photoMessage.style.color = "red";
                        photoMessage.textContent = data.error || "Failed to add photo.";
                        return;
                    }
                    photoMessage.style.color = "lightgreen";
                    photoMessage.textContent = "Photo added successfully.";
                    await loadPhotos();
                    photoUrlInput.value = "";
                } catch (err) {
                    console.error(err);
                    photoMessage.style.color = "red";
                    photoMessage.textContent = "Server error.";
                }
            });
        }
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
                    const res = await fetch(`/api/gyms/${gymId}/subscriptions`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
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
    loadPhotos();
    loadSubscriptions();
});
