document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("registerBtn");
    const msg = document.getElementById("registerMessage");
    btn.addEventListener("click", async () => {
        const role = document.getElementById("regRole").value;
        const username = document.getElementById("regUsername").value.trim();
        const email = document.getElementById("regEmail").value.trim();
        const password = document.getElementById("regPassword").value;
        if (!username || !email || !password) {
            msg.style.color = "red";
            msg.textContent = "Completează toate câmpurile.";
            return;
        }
        const res = await fetch("/api/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                name: username,
                username,
                email,
                password,
                role
            })
        });
        const data = await res.json();
        if (res.ok) {
            msg.style.color = "green";
            msg.textContent = data.message || "Account created";
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1000);
        } else {
            msg.style.color = "red";
            msg.textContent = data.error || "Registration failed";
        }
    });
});
