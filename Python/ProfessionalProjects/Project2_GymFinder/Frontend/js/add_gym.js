document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("saveGymBtn");
    const msg = document.getElementById("addGymMessage");
    if (!btn) return;
    btn.addEventListener("click", async () => {
        const gym_name       = document.getElementById("gymName").value.trim();
        const gym_owner_name = document.getElementById("gymOwnerName").value.trim();
        const country        = document.getElementById("country").value.trim();
        const district       = document.getElementById("district").value.trim();
        const city           = document.getElementById("city").value.trim();
        const street         = document.getElementById("street").value.trim();
        const street_number  = document.getElementById("streetNumber").value.trim();
        const google_maps_link = document.getElementById("mapsLink").value.trim();
        const size_m2_value         = document.getElementById("sizeM2").value;
        const description    = document.getElementById("description").value.trim();
        const has_locker_room = document.getElementById("hasLockerRoom").checked;
        const has_boxing      = document.getElementById("hasBoxing").checked;
        const has_sauna       = document.getElementById("hasSauna").checked;
        const has_pool        = document.getElementById("hasPool").checked;
        if (!gym_name || !gym_owner_name || !country || !district || !city || !street || !street_number) {
            msg.style.color = "red";
            msg.textContent = "Completează toate câmpurile obligatorii.";
            return;
        }
        const size_m2 = size_m2_value ? parseInt(size_m2_value, 10) : null;
        const ownerId = localStorage.getItem("gf_user_id");
    const payload = {
        gym_name,
        gym_owner_name,
        country,
        district,
        city,
        street,
        street_number,
        google_maps_link,
        description,
        size_m2,
        has_locker_room,
        has_boxing,
        has_sauna,
        has_pool,
        owner_id: ownerId
    };
        try {
            const res = await fetch("/api/gyms", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (res.ok) {
                msg.style.color = "lightgreen";
                msg.textContent = data.message || "Gym saved successfully!";
                setTimeout(() => {
                    window.location.href = "gym.html";
                }, 1000);
            } else {
                msg.style.color = "red";
                msg.textContent = data.error || "Failed to save gym.";
            }
        } catch (err) {
            console.error(err);
            msg.style.color = "red";
            msg.textContent = "Server error.";
        }
    });
});
