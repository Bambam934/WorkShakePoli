
const letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
// const board = document.getElementById('board'); // Ya no se usa
const wordInput = document.getElementById('wordInput');
const historialPalabras = document.getElementById('historialPalabras');
const scoreElement = document.getElementById('score');

let score = 0;
let letrasTablero = [];

// Generar tablero con letras desde el backend
function generarTablero() {
    letrasTablero = [...letrasDesdeBackend];  // Esto es importante para verificar palabras

    const board = document.createElement('div');
    board.className = 'tablero';

    letrasDesdeBackend.forEach(letra => {
        const letraElem = document.createElement('div');
        letraElem.className = 'letra';
        letraElem.textContent = letra.toUpperCase();
        board.appendChild(letraElem);
    });

    const container = document.querySelector('.container');
    const tableroExistente = document.querySelector('.tablero');
    if (tableroExistente) {
        container.removeChild(tableroExistente);
    }

    container.insertBefore(board, document.querySelector('#wordInput'));
}

// Verificar palabra ingresada
function verificarPalabra() {
    const palabra = wordInput.value.toUpperCase();

    if (palabra === '') {
        alert('Debes escribir una palabra');
        return;
    }

    if (!puedeFormarseConLetras(palabra)) {
        alert('La palabra no se puede formar con las letras del tablero');
        return;
    }

    if (diccionario.includes(palabra)) {
        agregarPalabraAlHistorial(palabra);
        aumentarPuntaje(palabra.length * 10);
    } else {
        alert('Palabra no encontrada en el diccionario');
    }

    wordInput.value = '';
}

// Verificar que la palabra se forme con las letras del tablero
function puedeFormarseConLetras(palabra) {
    const letrasDisponibles = [...letrasTablero];

    for (const letra of palabra) {
        const index = letrasDisponibles.indexOf(letra);
        if (index === -1) return false;
        letrasDisponibles.splice(index, 1);
    }
    return true;
}

// Mostrar palabra encontrada
function agregarPalabraAlHistorial(palabra) {
    if ([...historialPalabras.children].some(li => li.textContent === palabra)) {
        alert('Ya encontraste esta palabra');
        return;
    }

    const li = document.createElement('li');
    li.textContent = palabra;
    historialPalabras.appendChild(li);
}

// Aumentar puntaje
function aumentarPuntaje(puntos) {
    score += puntos;
    scoreElement.textContent = score;
}

// Mezclar letras
function mezclarLetras() {
    for (let i = letrasDesdeBackend.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [letrasDesdeBackend[i], letrasDesdeBackend[j]] = [letrasDesdeBackend[j], letrasDesdeBackend[i]];
    }
    generarTablero();  // regenerar con las letras mezcladas
}

let tiempoTotal = 180; // 3 minutos = 180 segundos
let tiempoRestante = tiempoTotal;

const cronometroSpan = document.getElementById("cronometro");
const barraProgreso = document.getElementById("barra-progreso");

function iniciarCronometro() {
    const intervalo = setInterval(() => {
        if (tiempoRestante <= 0) {
            clearInterval(intervalo);
            cronometroSpan.textContent = "00:00";
            barraProgreso.style.width = "0%";
            barraProgreso.style.backgroundColor = "#ff4444";
            alert("¡Tiempo terminado!");
            return;
        }

        tiempoRestante--;

        const minutos = String(Math.floor(tiempoRestante / 60)).padStart(2, "0");
        const segundos = String(tiempoRestante % 60).padStart(2, "0");
        cronometroSpan.textContent = `${minutos}:${segundos}`;

        const porcentaje = (tiempoRestante / tiempoTotal) * 100;
        barraProgreso.style.width = `${porcentaje}%`;

        // Cambio de color según porcentaje restante
        if (porcentaje > 60) {
            barraProgreso.style.backgroundColor = "#00ffcc"; // Cian
        } else if (porcentaje > 30) {
            barraProgreso.style.backgroundColor = "#ffcc00"; // Amarillo
        } else {
            barraProgreso.style.backgroundColor = "#ff4444"; // Rojo
        }
    }, 1000);
}


// Llamada al iniciar el juego
iniciarCronometro();


// Iniciar juego
generarTablero();
