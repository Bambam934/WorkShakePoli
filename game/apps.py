from django.apps import AppConfig

class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'  # ✅ Asegúrate de que el nombre sea el correcto
