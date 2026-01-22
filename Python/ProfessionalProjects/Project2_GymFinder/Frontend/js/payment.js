document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const subId = params.get("sub");
    const price = params.get("price");
    const paymentForm = document.getElementById("paymentForm");
    const msg = document.getElementById("paymentMessage");
    paymentForm.addEventListener("submit", (e) => {
        e.preventDefault();
        msg.style.color = "lightgreen";
        msg.textContent = "Payment simulated successfully 🙂";
        setTimeout(() => {
            window.location.href = "index.html";
        }, 1500);
    });
});
