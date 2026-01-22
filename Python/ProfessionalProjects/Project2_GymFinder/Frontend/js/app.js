function showAuthPanel(show) {
    const panel = document.getElementById("authPanel");
    if (show) panel.classList.remove("hidden");
    else panel.classList.add("hidden");
}

function renderRoleSection(role, username) {
    const sec = document.getElementById("roleSection");
    let title = "";
    let content = "";
    switch (role) {
        case "member":
            title = "Member dashboard";
            content = "Vezi sălile disponibile, compară abonamente și rezervă-ți locul.";
            break;
        case "gym_owner":
            title = "Gym Owner dashboard";
            content = "Gestionează-ți sala, abonamentele și vizualizează statisticile despre membri.";
            break;
        case "personal_trainer":
            title = "Personal Trainer dashboard";
            content = "Administrează-ți clienții, sesiunile de antrenament și programările.";
            break;
        case "nutrition_coach":
            title = "Nutrition Coach dashboard";
            content = "Configurează planuri alimentare și urmărește progresul clienților.";
            break;
        default:
            title = "Bine ai venit în GymFinder!";
            content = "Autentifică-te pentru a vedea interfața specifică rolului tău.";
    }
    sec.innerHTML = `
        <h2>${title}</h2>
        <p>${content}</p>
        ${username ? `<p><strong>Utilizator:</strong> ${username}</p>` : ""}
    `;
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("loginHeaderBtn").addEventListener("click", () => showAuthPanel(true));
    document.getElementById("signupHeaderBtn").addEventListener("click", () => showAuthPanel(true));
    document.getElementById("menuHeaderBtn").addEventListener("click", () => {
        alert("Aici poți deschide un meniu lateral cu opțiuni.");
    });
    document.getElementById("authPanel").addEventListener("click", (e) => {
        if (e.target.id === "authPanel") showAuthPanel(false);
    });
    document.getElementById("registerBtn").addEventListener("click", async () => {
        const name = document.getElementById("regName").value.trim();
        const username = document.getElementById("regUsername").value.trim();
        const email = document.getElementById("regEmail").value.trim();
        const password = document.getElementById("regPassword").value;
        const role = document.getElementById("regRole").value;
        const res = await fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, username, email, password, role })
        });
        const data = await res.json();
        const msgEl = document.getElementById("authMessage");
        if (res.ok) {
            msgEl.style.color = "green";
            msgEl.textContent = data.message;
        } else {
            msgEl.style.color = "red";
            msgEl.textContent = data.error || "Eroare la înregistrare";
        }
    });
    document.getElementById("loginBtn").addEventListener("click", async () => {
        const username = document.getElementById("loginUsername").value.trim();
        const password = document.getElementById("loginPassword").value;

        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        const msgEl = document.getElementById("authMessage");
        if (res.ok) {
            msgEl.style.color = "green";
            msgEl.textContent = `${data.message} (${data.role})`;
            localStorage.setItem("gf_username", data.username);
            localStorage.setItem("gf_role", data.role);
            renderRoleSection(data.role, data.username);
            showAuthPanel(false);
        } else {
            msgEl.style.color = "red";
            msgEl.textContent = data.error || "Eroare la autentificare";
        }
    });
    const savedRole = localStorage.getItem("gf_role");
    const savedUser = localStorage.getItem("gf_username");
    renderRoleSection(savedRole, savedUser);
});
