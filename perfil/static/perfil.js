document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const userCard = document.querySelector('.user-card');
    const imageContainer = document.querySelector('.image-container');
    const username = document.querySelector('.username');
    const lightModeButton = document.getElementById('light-mode');
    const darkModeButton = document.getElementById('dark-mode');
    const blueModeButton = document.getElementById('blue-mode');

    lightModeButton.addEventListener('click', () => {
        body.className = '';
        userCard.className = 'user-card';
        imageContainer.className = 'image-container';
        username.className = 'username';
    });

    darkModeButton.addEventListener('click', () => {
        body.className = 'dark-theme';
        userCard.className = 'user-card dark-theme';
        imageContainer.className = 'image-container dark-theme';
        username.className = 'username dark-theme';
    });

    blueModeButton.addEventListener('click', () => {
        body.className = 'blue-theme';
        userCard.className = 'user-card blue-theme';
        imageContainer.className = 'image-container blue-theme';
        username.className = 'username blue-theme';
    });
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