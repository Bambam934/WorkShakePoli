const letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const board = document.getElementById('board');
const wordInput = document.getElementById('wordInput');
const historialPalabras = document.getElementById('historialPalabras');
const scoreElement = document.getElementById('score');

let score = 0;
let letrasTablero = [];

// Diccionario de palabras válidas (simulación)
const diccionario = ['CASA', 'PERRO', 'GATO', 'SOL', 'LUNA', 'MAR', 'RIO', 'FLOR', 'ARBOL', 'FUEGO'];

// Generar letras aleatorias
function generarTablero() {
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
    letrasTablero.sort(() => Math.random() - 0.5);
    board.innerHTML = '';

    letrasTablero.forEach(letra => {
        const div = document.createElement('div');
        div.className = 'letra';
        div.textContent = letra;
        board.appendChild(div);
    });
}

// Iniciar juego
generarTablero();
