/*const letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const board = document.getElementById('board');
const wordInput = document.getElementById('wordInput');
const historialPalabras = document.getElementById('historialPalabras');
const scoreElement = document.getElementById('score');

let score = 0;
let letrasTablero = [];


// Generar letras aleatorias
/*function generarTablero() {
    letrasTablero = [];
    board.innerHTML = '';

    for (let i = 0; i < 25; i++) {
        const letra = letras.charAt(Math.floor(Math.random() * letras.length));
        letrasTablero.push(letra);

        const div = document.createElement('div');
        div.className = 'letra';
        div.textContent = letra;
        board.appendChild(div);
    }
}
function generarTablero() {
    // Usa las letras ya pasadas desde el backend
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
    // Mezclar las letras actuales del backend
    for (let i = letrasDesdeBackend.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [letrasDesdeBackend[i], letrasDesdeBackend[j]] = [letrasDesdeBackend[j], letrasDesdeBackend[i]];
    }
    generarTablero();  // regenerar con las letras mezcladas
}

function agregarPalabraAlHistorial(palabra) {
    if ([...historialPalabras.children].some(li => li.textContent === palabra)) {
        alert('Ya encontraste esta palabra');
        return;
    }

    const li = document.createElement('li');
    li.textContent = palabra;
    historialPalabras.appendChild(li);
}
// Iniciar juego
generarTablero(); */
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

let segundos = 0;
let minutos = 0;
const cronometroElemento = document.getElementById("cronometro");

function actualizarCronometro() {
    segundos++;
    if (segundos === 60) {
        segundos = 0;
        minutos++;
    }

    const minStr = minutos < 10 ? "0" + minutos : minutos;
    const segStr = segundos < 10 ? "0" + segundos : segundos;

    cronometroElemento.textContent = `${minStr}:${segStr}`;
}

const intervaloCronometro = setInterval(actualizarCronometro, 1000);

// Iniciar juego
generarTablero();
