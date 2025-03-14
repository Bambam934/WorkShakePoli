from django.db import models
from django.conf import settings  # ✅ Importa settings correctamente

class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Relación corregida
    word = models.CharField(max_length=50)
    points = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.word} ({self.points} pts)"  # ✅ Usamos email porque es el identificador

