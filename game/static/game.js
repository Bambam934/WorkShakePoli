/* static/game.js — cargado con defer */

/* Elementos del DOM */
const wordInput = document.getElementById('wordInput');
const historialPalabras = document.getElementById('historialPalabras');
const scoreElement = document.getElementById('score');
const cronometroSpan = document.getElementById('cronometro');
const barraProgreso = document.getElementById('barra-progreso');

let score = 0;
let letrasTablero = [];

/* ---------- Tablero ---------- */
function generarTablero() {
    if (!Array.isArray(letrasDesdeBackend) || letrasDesdeBackend.length === 0) {
        console.error('letrasDesdeBackend no es un array:', letrasDesdeBackend);
        return;
    }
    letrasTablero = [...letrasDesdeBackend];

    const board = document.createElement('div');
    board.className = 'tablero';

    letrasDesdeBackend.forEach(l => {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.textContent = l;
        board.appendChild(cell);
    });

    const container = document.querySelector('.container');
    const anterior = document.querySelector('.tablero');
    if (anterior) container.removeChild(anterior);
    container.insertBefore(board, wordInput);
}

/* ---------- Lógica de palabras ---------- */
function puedeFormarseConLetras(pal) {
    const disp = [...letrasTablero];
    for (const l of pal) {
        const i = disp.indexOf(l);
        if (i === -1) return false;
        disp.splice(i, 1);
    }
    return true;
}
function agregarPalabra(pal) {
    const li = document.createElement('li');
    li.textContent = pal;
    historialPalabras.appendChild(li);
}
function aumentarPuntaje(p) { score += p; scoreElement.textContent = score; }

function verificarPalabra() {
    const pal = wordInput.value.trim().toUpperCase();
    if (!pal) return alert('Debes escribir una palabra');
    if (!puedeFormarseConLetras(pal)) return alert('No puedes formar esa palabra');
    if (!diccionario.includes(pal)) return alert('Palabra no reconocida');
    if ([...historialPalabras.children].some(li => li.textContent === pal))
        return alert('Ya encontraste esta palabra');

    agregarPalabra(pal);
    aumentarPuntaje(pal.length * 10);
    wordInput.value = '';
}

function mezclarLetras() {
    for (let i = letrasDesdeBackend.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [letrasDesdeBackend[i], letrasDesdeBackend[j]] =
            [letrasDesdeBackend[j], letrasDesdeBackend[i]];
    }
    generarTablero();
}

/* ---------- Cronómetro ---------- */
let tiempoTotal = 180;
let tiempoRestante = tiempoTotal;

function iniciarCronometro() {
    const intv = setInterval(() => {
        if (--tiempoRestante < 0) {
            clearInterval(intv);
            cronometroSpan.textContent = '00:00';
            barraProgreso.style.width = '0%';
            barraProgreso.style.backgroundColor = '#ff4444';
            alert('¡Tiempo terminado!');
            return;
        }
        const m = String(Math.floor(tiempoRestante / 60)).padStart(2, '0');
        const s = String(tiempoRestante % 60).padStart(2, '0');
        cronometroSpan.textContent = `${m}:${s}`;

        const pct = (tiempoRestante / tiempoTotal) * 100;
        barraProgreso.style.width = `${pct}%`;
        barraProgreso.style.backgroundColor =
            pct > 60 ? '#00ffcc' : pct > 30 ? '#ffcc00' : '#ff4444';
    }, 1000);
}

/* ---------- Init ---------- */
document.addEventListener('DOMContentLoaded', () => {
    generarTablero();
    iniciarCronometro();
    wordInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') { e.preventDefault(); verificarPalabra(); }
    });
});
