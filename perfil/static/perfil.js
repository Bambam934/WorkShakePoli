document.addEventListener('DOMContentLoaded', function() {
    const root = document.documentElement;

    const neonButtons = {
        'red-theme': '#ff4d4d',
        'white-theme': '#f4f4f4',
        'green-theme': '#00ff66',
        'blue-theme': '#00aaff'
    };

    // Función para obtener el token CSRF de la cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Aplicar y guardar color al hacer clic en botón
    for (const [id, color] of Object.entries(neonButtons)) {
        const btn = document.getElementById(id);
        if (btn) {
            btn.addEventListener('click', () => {
                root.style.setProperty('--neon-color', color);

                // Enviar el color al servidor
                fetch('/update-color/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: `color=${encodeURIComponent(color)}`
                })
                .then(response => {
                    if (!response.ok) {
                        console.error('Error al guardar el color');
                    }
                })
                .catch(error => {
                    console.error('Error de red:', error);
                });
            });
        }
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const profilePictureInput = document.getElementById('profile-picture-input');
    const uploadForm = document.querySelector('form'); // Selecciona el formulario

    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function() {
            // Enviar el formulario automáticamente cuando se selecciona un archivo
            uploadForm.submit();
        });
    }
});
