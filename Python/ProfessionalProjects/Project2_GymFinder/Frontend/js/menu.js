document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("menuToggle");
    const menu = document.getElementById("sideMenu");
    if (!btn || !menu) return;
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        menu.style.display = (menu.style.display === "flex") ? "none" : "flex";
    });
    document.addEventListener("click", (e) => {
        if (!menu.contains(e.target) && e.target !== btn) {
            menu.style.display = "none";
        }
    });
});
