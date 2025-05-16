// static/game/js/game.js
import { saveScore } from './leaderboard.js';

/* ---------- Inyectados desde game.html ---------- */
const partidaUrl = window.partidaUrl;
const redireccionURL = window.redireccionURL;
const letrasDesdeBackend = window.letrasDesdeBackend;
const diccionario = window.diccionario;

/* ---------- Elementos del DOM ---------- */
const wordInput = document.getElementById('wordInput');
const historialPalabras = document.getElementById('historialPalabras');
const scoreElement = document.getElementById('score');
const cronometroSpan = document.getElementById('cronometro');
const barraProgreso = document.getElementById('barra-progreso');

/* ---------- Variables de juego ---------- */
let score = 0;
let letrasTablero = [];
let palabraActual = "";

/* ---------- TABLERO ---------- */
function generarTablero() {
    if (!Array.isArray(letrasDesdeBackend) || !letrasDesdeBackend.length) {
        console.error('letrasDesdeBackend no es un array:', letrasDesdeBackend);
        return;
    }
    letrasTablero = [...letrasDesdeBackend];
    palabraActual = "";
    wordInput.value = "";

    const board = document.createElement('div');
    board.className = 'tablero';
    letrasDesdeBackend.forEach(letra => {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.textContent = letra;
        cell.addEventListener('click', () => toggleCell(cell, letra));
        board.appendChild(cell);
    });

    const container = document.querySelector('.container');
    const anterior = document.querySelector('.tablero');
    if (anterior) container.removeChild(anterior);
    container.insertBefore(board, wordInput);
}

function toggleCell(cell, letra) {
    cell.classList.toggle('selected');
    if (cell.classList.contains('selected')) {
        palabraActual += letra;
    } else {
        const i = palabraActual.indexOf(letra);
        if (i !== -1) {
            palabraActual = palabraActual.slice(0, i) + palabraActual.slice(i + 1);
        }
    }
    wordInput.value = palabraActual;
}

/* ---------- LÓGICA DE PALABRAS ---------- */
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

function aumentarPuntaje(p) {
    score += p;
    scoreElement.textContent = score;
}

function verificarPalabra() {
    const pal = wordInput.value.trim().toUpperCase();
    if (!pal) return alert('Debes escribir una palabra');
    if (!puedeFormarseConLetras(pal)) return alert('No puedes formar esa palabra');
    if (!diccionario.includes(pal)) return alert('Palabra no reconocida');
    if ([...historialPalabras.children].some(li => li.textContent === pal))
        return alert('Ya encontraste esta palabra');

    agregarPalabra(pal);
    aumentarPuntaje(pal.length * 10);
    palabraActual = "";
    wordInput.value = "";
    document.querySelectorAll('.cell.selected')
        .forEach(c => c.classList.remove('selected'));
}

function mezclarLetras() {
    for (let i = letrasDesdeBackend.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [letrasDesdeBackend[i], letrasDesdeBackend[j]] =
            [letrasDesdeBackend[j], letrasDesdeBackend[i]];
    }
    generarTablero();
}

/* ---------- CRONÓMETRO ---------- */
const tiempoTotal = 180;
let tiempoRestante = tiempoTotal;
let cronometroIntv = null;
function iniciarCronometro() {
    cronometroIntv = setInterval(() => {
        if (--tiempoRestante < 0) {
            clearInterval(cronometroIntv);
            cronometroSpan.textContent = '00:00';
            barraProgreso.style.width = '0%';
            barraProgreso.style.background = '#ff4444';
            alert('¡Tiempo terminado!');
            endGame(score);
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

/* ---------- INICIALIZACIÓN ---------- */
document.addEventListener('DOMContentLoaded', () => {
    generarTablero();
    iniciarCronometro();
    wordInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
            e.preventDefault();
            verificarPalabra();
        }
    });
    document.getElementById('btn-verificar')
        .addEventListener('click', verificarPalabra);
    document.getElementById('btn-mezclar')
        .addEventListener('click', mezclarLetras);
});

/* ---------- CSRF Helper ---------- */
function getCookie(name) {
    return document.cookie.split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
}
const csrftoken = getCookie('csrftoken');

/* ---------- FIN DE PARTIDA & PUNTAJE ---------- */
async function endGame(finalScore) {
    const name = prompt('Ingresa tu nombre:');
    if (name) saveScore(name, finalScore);

    try {
        const resp = await fetch(partidaUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                score: finalScore,
                words: historialPalabras.children.length,
            }),
        });
        if (!resp.ok) console.error('Error guardando partida:', resp.status);
    } catch (err) {
        console.error('Error de red al enviar partida:', err);
    }

    // al terminar, redirigimos fuera del juego
    window.location.href = redireccionURL;
}

// Exponer endGame globalmente (lo llama el cronómetro)
window.endGame = endGame;
window.verificarPalabra = verificarPalabra;
window.mezclarLetras = mezclarLetras;
