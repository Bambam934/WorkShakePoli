/**
 * modal.js - Gestión avanzada del leaderboard modal
 * 
 * Características principales:
 * - Animaciones mejoradas con efectos de entrada/salida
 * - Manejo de errores robusto
 * - Sistema de eventos personalizados
 * - Soporte para temas dinámicos
 * - Optimización de rendimiento
 * - Mejor accesibilidad
 * 
 * Requiere:
 * - Botón con id="btn-show-leaderboard"
 * - Dialog con id="dlg-leaderboard"
 * - Sección de contenido con id="dlg-content"
 * - Función getScores() de leaderboard.js
 */

import { getScores } from './leaderboard.js';

// Constantes de configuración
const CONFIG = {
    animationDuration: {
        open: 200,
        close: 150
    },
    maxItems: 10,
    localStorageKey: 'leaderboard-scores'
};

// Referencias al DOM
const dom = {
    btnShow: document.getElementById('btn-show-leaderboard'),
    dialog: document.getElementById('dlg-leaderboard'),
    content: document.getElementById('dlg-content'),
    title: document.querySelector('#dlg-leaderboard h2')
};

// Estado del modal
const state = {
    isOpen: false,
    currentAnimation: null
};

/* ---------- Renderizado del ranking ---------- */
async function renderLeaderboard() {
    try {
        // Mostrar estado de carga
        dom.content.innerHTML = '<div class="loading">Cargando...</div>';
        
        const data = await getScores();
        dom.content.innerHTML = '';

        if (!data || !data.length) {
            showEmptyState();
            return;
        }

        const limitedData = data.slice(0, CONFIG.maxItems);
        createList(limitedData);
        
        // Disparar evento personalizado
        document.dispatchEvent(new CustomEvent('leaderboardRendered', {
            detail: { itemCount: limitedData.length }
        }));
        
    } catch (error) {
        console.error('Error al renderizar el leaderboard:', error);
        showErrorState();
    }
}

function createList(data) {
    const list = document.createElement('ol');
    list.setAttribute('aria-label', 'Lista de puntuaciones');

    data.forEach(({ name, score }, index) => {
        const li = document.createElement('li');
        li.setAttribute('aria-posinset', index + 1);
        li.setAttribute('aria-setsize', data.length);
        li.classList.add('rank-' + (index + 1)); 

        li.innerHTML = `
            <span class="rank">${index + 1}.</span>
            <strong class="name">${escapeHTML(name)}</strong>
            <span class="score">${score}</span>
        `;
        list.appendChild(li);
    });

    dom.content.appendChild(list);
}


function showEmptyState() {
    dom.content.innerHTML = `
        <div class="empty-state">
            <svg aria-hidden="true" width="48" height="48" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            <p>Sin registros todavía.</p>
        </div>
    `;
}

function showErrorState() {
    dom.content.innerHTML = `
        <div class="error-state">
            <svg aria-hidden="true" width="48" height="48" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            <p>Error al cargar los puntajes.</p>
            <button id="retry-loading" class="retry-btn">Reintentar</button>
        </div>
    `;
    
    document.getElementById('retry-loading')?.addEventListener('click', renderLeaderboard);
}

/* ---------- Animaciones ---------- */
function animateOpen() {
    // Cancelar animación previa si existe
    if (state.currentAnimation) {
        state.currentAnimation.cancel();
    }

    state.currentAnimation = dom.dialog.animate(
        [
            { transform: 'translateY(20px) scale(0.95)', opacity: 0 },
            { transform: 'translateY(0) scale(1)', opacity: 1 }
        ],
        {
            duration: CONFIG.animationDuration.open,
            easing: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
            fill: 'forwards'
        }
    );

    // Animar backdrop
    dom.dialog.parentElement.animate(
        [{ opacity: 0 }, { opacity: 1 }],
        { duration: CONFIG.animationDuration.open, easing: 'ease-out' }
    );

    state.currentAnimation.onfinish = () => {
        state.isOpen = true;
        state.currentAnimation = null;
    };
}

function animateClose() {
    if (state.currentAnimation) {
        state.currentAnimation.cancel();
    }

    state.currentAnimation = dom.dialog.animate(
        [
            { transform: 'translateY(0) scale(1)', opacity: 1 },
            { transform: 'translateY(20px) scale(0.95)', opacity: 0 }
        ],
        {
            duration: CONFIG.animationDuration.close,
            easing: 'ease-in',
            fill: 'forwards'
        }
    );

    // Animar backdrop
    dom.dialog.parentElement.animate(
        [{ opacity: 1 }, { opacity: 0 }],
        { duration: CONFIG.animationDuration.close, easing: 'ease-in' }
    );

    state.currentAnimation.onfinish = () => {
        dom.dialog.close();
        state.isOpen = false;
        state.currentAnimation = null;
    };
}

/* ---------- Manejo del Modal ---------- */
function openModal() {
    if (state.isOpen) return;
    
    dom.dialog.showModal();
    renderLeaderboard();
    animateOpen();
    
    // Enfocar el primer elemento interactivo
    setTimeout(() => {
        const firstInteractive = dom.dialog.querySelector('button, [tabindex]');
        firstInteractive?.focus();
    }, CONFIG.animationDuration.open);
}

function closeModal() {
    if (!state.isOpen) return;
    animateClose();
}

/* ---------- Eventos ---------- */
function setupEventListeners() {
    // Abrir modal
    dom.btnShow?.addEventListener('click', openModal);
    
    // Cerrar al hacer clic fuera
    dom.dialog.addEventListener('click', (e) => {
        if (e.target === dom.dialog) closeModal();
    });
    
    // Cerrar con ESC
    dom.dialog.addEventListener('cancel', (e) => {
        e.preventDefault();
        closeModal();
    });
    
    // Cerrar con el botón del formulario
    dom.dialog.querySelector('form')?.addEventListener('submit', (e) => {
        e.preventDefault();
        closeModal();
    });
    
    // Mejorar accesibilidad
    dom.dialog.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            const focusable = [...dom.dialog.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')];
            
            if (focusable.length === 0) return;
            
            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            
            if (e.shiftKey && document.activeElement === first) {
                last.focus();
                e.preventDefault();
            } else if (!e.shiftKey && document.activeElement === last) {
                first.focus();
                e.preventDefault();
            }
        }
    });
}

/* ---------- Utilidades ---------- */
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/* ---------- Inicialización ---------- */
function init() {
    if (!dom.dialog) {
        console.warn('No se encontró el elemento dialog');
        return;
    }
    
    setupEventListeners();
    
    // Configuración inicial del modal
    dom.dialog.setAttribute('aria-labelledby', 'leaderboard-title');
    dom.dialog.setAttribute('aria-modal', 'true');
    dom.dialog.setAttribute('role', 'dialog');
    dom.title.id = 'leaderboard-title';
}

// Iniciar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

/* ---------- API Pública ---------- */
export const LeaderboardModal = {
    open: openModal,
    close: closeModal,
    refresh: renderLeaderboard
};

// Para depuración
window.LeaderboardModal = LeaderboardModal;