/*  modal.js
 *  =========
 *  Muestra el leaderboard en un <dialog> flotante dentro de la pantalla
 *  de selección de niveles.
 *
 *  • Requiere que en el HTML existan:
 *      <button id="btn-show-leaderboard">…</button>
 *      <dialog  id="dlg-leaderboard">
 *          <form method="dialog">
 *              <h2>Top 10</h2>
 *              <section id="dlg-content"></section>
 *              <menu><button>Cerrar</button></menu>
 *          </form>
 *      </dialog>
 *
 *  • Usa getScores() de leaderboard.js (localStorage) – no toca el backend.
 */

import { getScores } from './leaderboard.js';

/* ---------- Referencias al DOM ---------- */
const btnShow = document.getElementById('btn-show-leaderboard');
const dialog = document.getElementById('dlg-leaderboard');
const area = document.getElementById('dlg-content');

/* ---------- Render del ranking ---------- */
function renderLeaderboard() {
    const data = getScores();            // [{ name, score }, …]

    area.innerHTML = '';                 // limpia

    if (!data.length) {
        area.textContent = 'Sin registros todavía.';
        return;
    }

    const list = document.createElement('ol');
    data.forEach(({ name, score }) => {
        const li = document.createElement('li');
        li.innerHTML = `
      <strong>${name}</strong>
      <span class="score">— ${score}</span>
    `;
        list.appendChild(li);
    });

    area.appendChild(list);
}

/* ---------- Animaciones ---------- */
function animateOpen() {
    dialog.animate(
        [{ transform: 'scale(0.7)', opacity: 0 },
        { transform: 'scale(1)', opacity: 1 }],
        { duration: 180, easing: 'ease-out' }
    );
}
function animateClose() {
    // Se ejecuta antes de cerrar para lograr efecto “zoom‑out”
    const anim = dialog.animate(
        [{ transform: 'scale(1)', opacity: 1 },
        { transform: 'scale(0.6)', opacity: 0 }],
        { duration: 150, easing: 'ease-in' }
    );
    anim.addEventListener('finish', () => dialog.close());
}

/* ---------- Eventos ---------- */
btnShow?.addEventListener('click', () => {
    renderLeaderboard();
    dialog.showModal();
    animateOpen();
});

dialog.addEventListener('click', e => {
    if (e.target === dialog) animateClose();   // clic fuera
});

dialog.addEventListener('cancel', e => {
    e.preventDefault();                        // evita cierre instantáneo (ESC)
    animateClose();
});

/* ---------- (Opcional) Exponer para debug ---------- */
window.renderLeaderboard = renderLeaderboard;
