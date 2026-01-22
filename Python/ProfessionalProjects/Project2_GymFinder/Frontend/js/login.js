document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("loginBtn");
    const msg = document.getElementById("loginMessage");
    btn.addEventListener("click", async () => {
        const username = document.getElementById("loginUsername").value.trim();
        const password = document.getElementById("loginPassword").value;
        if (!username || !password) {
            msg.style.color = "red";
            msg.textContent = "Completează username și parola.";
            return;
        }
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem("gf_logged_in", "true");
            localStorage.setItem("gf_username", data.username);
            localStorage.setItem("gf_role", data.role);
            localStorage.setItem("gf_user_id", data.id);
            window.location.href = "index.html";
        } else {
            msg.style.color = "red";
            msg.textContent = data.error || "Login failed";
        }
    });
});
