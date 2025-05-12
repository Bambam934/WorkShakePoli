// perfil/static/perfil/js/perfil.js

document.addEventListener('DOMContentLoaded', () => {
    const root = document.documentElement;

    // 1) Mapa de botones → color
    const neonButtons = {
        'red-theme': '#ff4d4d',
        'white-theme': '#f4f4f4',
        'green-theme': '#00ff66',
        'blue-theme': '#00aaff'
    };

    // 2) CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                }
            });
        }
        return cookieValue;
    }
    const csrfToken = getCookie('csrftoken');

    // 3) URL dinámica del endpoint de color
    const colorUrl = "{% url 'update_neon_color' %}";

    // 4) Conectar cada botón de tema
    Object.entries(neonButtons).forEach(([btnId, color]) => {
        const btn = document.getElementById(btnId);
        if (!btn) return;
        btn.addEventListener('click', () => {
            // cambiar variable CSS
            root.style.setProperty('--neon-color', color);

            // notificar al servidor
            fetch(colorUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `color=${encodeURIComponent(color)}`
            })
                .then(res => {
                    if (!res.ok) console.error('Error guardando color');
                })
                .catch(e => console.error('Error de red:', e));
        });
    });

    // 5) Auto-submit del form de foto de perfil
    const uploadInput = document.getElementById('profile-picture-input');
    const uploadForm = document.getElementById('form-upload');
    if (uploadInput && uploadForm) {
        uploadInput.addEventListener('change', () => uploadForm.submit());
    }
});
