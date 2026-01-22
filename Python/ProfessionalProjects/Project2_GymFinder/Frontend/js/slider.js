document.addEventListener("DOMContentLoaded", () => {
    const slides = document.querySelectorAll(".slide");
    if (!slides.length) return;
    let current = 0;
    function nextSlide() {
        slides[current].classList.remove("active");
        current = (current + 1) % slides.length;
        slides[current].classList.add("active");
    }
    setInterval(nextSlide, 4000);
});
