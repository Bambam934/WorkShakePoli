document.addEventListener('DOMContentLoaded', function() {
    const root = document.documentElement;

    const neonButtons = {
        'red-theme': '#ff4d4d',
        'white-theme': '#f4f4f4',
        'green-theme': '#00ff66',
        'blue-theme': '#00aaff'
    };

    for (const [id, color] of Object.entries(neonButtons)) {
        const btn = document.getElementById(id);
        if (btn) {
            btn.addEventListener('click', () => {
                root.style.setProperty('--neon-color', color);
            });
        }
    }

    // Subida automática de imagen
    const profilePictureInput = document.getElementById('profile-picture-input');
    const uploadForm = document.querySelector('form');

    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function() {
            uploadForm.submit();
        });
    }
});
