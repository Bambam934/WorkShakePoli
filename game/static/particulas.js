document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('particle-container');
    if (!container) return;                       // ⬅ evita error

    const words = ["WordShake", "Juego", "Nivel", "¡Vamos!"];
    for (let i = 0; i < 50; i++) {
        const span = document.createElement("span");
        span.className = "particle";
        span.textContent = words[Math.floor(Math.random() * words.length)];
        span.style.left = `${Math.random() * 100}vw`;
        span.style.top = `${Math.random() * 100}vh`;
        span.style.animationDuration = `${5 + Math.random() * 10}s`;
        container.appendChild(span);
    }
});