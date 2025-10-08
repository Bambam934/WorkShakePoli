# game/admin.py
from django.contrib import admin, messages
from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _
import requests

from django.contrib.admin.helpers import ActionForm  
from .models import Word, Score, Game, Submission
from categorias.models import Level

# -------- Helpers --------

def validar_palabra_local(text: str) -> bool:
    """
    Validador sencillo y rápido: solo letras y longitud >= 2.
    Cambia por tu lógica real o por services.check_word_api si lo prefieres.
    """
    t = (text or "").strip().upper()
    return len(t) >= 2 and t.isalpha()

def validar_palabra_api(text: str, timeout=4) -> bool:
    """
    Ejemplo con dictionaryapi.dev (EN). Si usas otro diccionario, cámbialo aquí.
    """
    try:
        r = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{text.lower()}",
            timeout=timeout,
        )
        return r.status_code == 200
    except requests.RequestException:
        return False

# -------- Action form para importar --------

class ImportActionForm(ActionForm):  # 👈 hereda de ActionForm, no de forms.Form
    patron = forms.CharField(
        label="Patrón Datamuse (sp= patrón, ej: ab??)",
        required=False,
        help_text="Se usa con ?=cualquier letra, *=cualquier secuencia. Ej: ab??, *cion",
    )
    max_n = forms.IntegerField(
        label="Límite",
        required=False,
        min_value=1,
        max_value=1000,
        initial=50,
        help_text="Máximo de palabras a traer.",
    )
    level = forms.ModelChoiceField(
        label="Asignar al nivel (opcional)",
        queryset=Level.objects.all(),
        required=False,
        help_text="Si seleccionas un nivel, las nuevas palabras quedarán ligadas a él.",
    )
    marcar_validadas = forms.BooleanField(
        label="Marcar como validadas",
        required=False,
        initial=True,
    )
# -------- Admin de Word --------

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("text", "is_validated", "is_from_api", "niveles_")
    list_filter  = ("is_validated", "is_from_api", "levels")
    search_fields = ("text",)
    ordering = ("text",)
    filter_horizontal = ("levels",)

    # acciones
    actions = ["importar_desde_datamuse", "validar_seleccionadas", "marcar_como_no_validas"]
    action_form = ImportActionForm

    def niveles_(self, obj):
        return ", ".join(obj.levels.values_list("name", flat=True))
    niveles_.short_description = "Niveles"

    @admin.action(description="Importar desde Datamuse (usa campos del formulario de acciones)")
    def importar_desde_datamuse(self, request, queryset):
        patron = request.POST.get("patron", "").strip()
        try:
            max_n = int(request.POST.get("max_n") or 50)
        except ValueError:
            max_n = 50
        level_id = request.POST.get("level") or None
        marcar_validadas = bool(request.POST.get("marcar_validadas"))

        if not patron:
            self.message_user(request, "Debes indicar un patrón (campo 'patrón').", level=messages.WARNING)
            return

        # Llamada Datamuse (sp = patrón por letras)
        url = "https://api.datamuse.com/words"
        params = {"sp": patron, "max": max_n}
        try:
            resp = requests.get(url, params=params, timeout=6)
            resp.raise_for_status()
            items = resp.json()
        except requests.RequestException as e:
            self.message_user(request, f"Error consultando Datamuse: {e}", level=messages.ERROR)
            return

        # Crear/actualizar palabras
        creadas = 0
        ya_existian = 0
        with transaction.atomic():
            for it in items:
                w = (it.get("word") or "").strip().upper()
                if not w or not w.isalpha():
                    continue

                obj, created = Word.objects.get_or_create(
                    text=w,
                    defaults={
                        "is_from_api": True,
                        "is_validated": marcar_validadas and validar_palabra_local(w),
                    },
                )
                if not created:
                    ya_existian += 1
                else:
                    creadas += 1
                    if level_id:
                        try:
                            lvl = Level.objects.get(pk=level_id)
                            obj.levels.add(lvl)
                        except Level.DoesNotExist:
                            pass

        self.message_user(
            request,
            f"Importación lista. Creadas: {creadas}, ya existían: {ya_existian}.",
            level=messages.SUCCESS,
        )

    @admin.action(description="Validar seleccionadas (marca is_validated=True si pasan)")
    def validar_seleccionadas(self, request, queryset):
        actualizadas = 0
        for w in queryset:
            # combina validación local rápida + (opcional) validación API
            ok_local = validar_palabra_local(w.text)
            ok_api = True  # cambia a validar_palabra_api(w.text) si quieres llamar API real
            if ok_local and ok_api and not w.is_validated:
                w.is_validated = True
                w.save(update_fields=["is_validated"])
                actualizadas += 1
        self.message_user(
            request,
            f"Validación lista. Marcadas como válidas: {actualizadas}.",
            level=messages.SUCCESS,
        )

    @admin.action(description="Marcar seleccionadas como NO válidas")
    def marcar_como_no_validas(self, request, queryset):
        n = queryset.update(is_validated=False)
        self.message_user(request, f"{n} palabras marcadas como no válidas.", level=messages.INFO)

# -------- Admin de Game / Submission / Score --------

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "status", "total_score", "created_at", "finished_at")
    list_filter  = ("status", "created_at")
    search_fields = ("player__email",)
    readonly_fields = ("created_at", "finished_at")
    ordering = ("-created_at",)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "word", "accepted", "delta", "created_at")
    list_filter  = ("accepted", "created_at")
    search_fields = ("word", "game__player__email")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("user", "word", "points", "date")
    list_filter  = ("date",)
    search_fields = ("user__email", "word")
    ordering = ("-date",)
