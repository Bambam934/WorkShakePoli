document.addEventListener("DOMContentLoaded", () => {
    const words = ["WordShake", "Letra", "Juego", "Nivel", "Categoría", "¡Vamos!", "Score", "ABC"];
    const container = document.getElementById("particle-container");

    for (let i = 0; i < 50; i++) {
        const word = document.createElement("span");
        word.classList.add("particle");
        word.textContent = words[Math.floor(Math.random() * words.length)];
        word.style.left = `${Math.random() * 100}vw`;
        word.style.top = `${Math.random() * 100}vh`;
        word.style.animationDuration = `${5 + Math.random() * 10}s`;
        word.style.fontSize = `${12 + Math.random() * 18}px`;
        container.appendChild(word);
    }
});
