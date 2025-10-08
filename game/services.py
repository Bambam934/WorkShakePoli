# game/services.py
import random
import string
import logging
import httpx
from datetime import timedelta
from django.core.cache import cache
from django.utils import timezone
from collections import Counter
from categorias.models import Category, Level
from .models import Word

logger = logging.getLogger(__name__)

# Puntuación estilo Scrabble (ES)
LETTER_POINTS = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
    'I': 1, 'J': 8, 'K': 8, 'L': 1, 'M': 3, 'N': 1, '\u00D1': 8, 'O': 1,
    'P': 3, 'Q': 5, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 10,
    'X': 8, 'Y': 4, 'Z': 10
}

# =========================
# Tableros
# =========================
def generate_board(size: int = 25) -> str:
    """Genera un tablero de letras pseudo-aleatorias (por defecto 5x5 = 25)."""
    alphabet = string.ascii_uppercase.replace('Ñ', '') + 'Ñ'
    return "".join(random.choice(alphabet) for _ in range(size))

def generate_board_with_required_letters(words_queryset, size: int = 25) -> str:
    """
    Genera un tablero asegurando que aparezcan letras de un conjunto de palabras.
    Recibe un QuerySet de Word (o iterables con .text).
    """
    palabras = [getattr(w, "text", str(w)).upper() for w in words_queryset]
    if not palabras:
        return generate_board(size)

    random.shuffle(palabras)
    seleccion = palabras[: min(5, len(palabras))]

    letras = []
    for p in seleccion:
        letras.extend(list(p))

    alphabet = string.ascii_uppercase.replace('Ñ', '') + 'Ñ'
    while len(letras) < size:
        letras.append(random.choice(alphabet))

    random.shuffle(letras)
    return "".join(letras)

def generate_custom_game_board(categoria_name: str, nivel_name: str, size: int = 25) -> str:
    """
    Busca palabras del Level y genera un tablero que incluya sus letras.
    Si el nivel no tiene palabras, retorna aleatorio.
    """
    try:
        categoria = Category.objects.get(name=categoria_name)
        nivel = Level.objects.get(name=nivel_name, category=categoria)
        words_in_level = Word.objects.filter(levels=nivel)
    except (Category.DoesNotExist, Level.DoesNotExist):
        words_in_level = Word.objects.none()

    if words_in_level.exists():
        return generate_board_with_required_letters(words_in_level, size=size)
    return generate_board(size=size)

# =========================
# Validación de palabras
# =========================
DICTIONARY_API_ES = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"  # puedes cambiar a otro dict

def _cache_key(word: str) -> str:
    return f"word_validation::{word.upper()}"

def is_word_valid_local(word: str) -> bool:
    """Valida por base local (tabla Word.is_validated)."""
    w = (word or "").strip().upper()
    if not w.isalpha() or len(w) < 2:
        return False
    try:
        obj = Word.objects.get(text=w)
        return bool(obj.is_validated)
    except Word.DoesNotExist:
        return False

def is_word_valid_external(word: str, timeout=5.0) -> bool:
    """
    Valida contra API externa y persiste el resultado en Word.
    Usa httpx (ya disponible) y cachea 24h.
    """
    w = (word or "").strip().upper()
    if not w.isalpha() or len(w) < 2:
        return False

    ckey = _cache_key(w)
    cached = cache.get(ckey)
    if cached is not None:
        return bool(cached)

    url = DICTIONARY_API_ES.format(word=w.lower())
    try:
        r = httpx.get(url, timeout=timeout)
    except httpx.HTTPError as e:
        logger.warning(f"Dictionary API error: {e}")
        cache.set(ckey, False, 60)  # cache corto ante error
        return False

    if r.status_code == 200:
        Word.objects.update_or_create(
            text=w, defaults={"is_validated": True, "is_from_api": True}
        )
        cache.set(ckey, True, 24 * 3600)
        return True

    # Marcar como no válida para no consultar repetido
    Word.objects.update_or_create(
        text=w, defaults={"is_validated": False, "is_from_api": True}
    )
    cache.set(ckey, False, 24 * 3600)
    return False

def is_word_valid(word: str) -> bool:
    """
    Estrategia de validación: primero local; si no existe, consulta API externa.
    """
    if is_word_valid_local(word):
        return True
    return is_word_valid_external(word)

# =========================
# Puntaje
# =========================
def score_word(word: str) -> int:
    """Suma por letra + bonus simple por longitud."""
    w = (word or "").strip().upper()
    base = sum(LETTER_POINTS.get(ch, 0) for ch in w)
    bonus = 3 if len(w) >= 5 else 0
    return base + bonus

# (Opcional) multiplicadores por nivel/categoría:
def score_word_with_context(word: str, levels_qs=None) -> int:
    """
    Puntaje con multiplicadores según Level (si lo necesitas).
    Por ejemplo, si algún Level asociado se llama 'Premium' => x1.5
    """
    score = score_word(word)
    try:
        wobj = Word.objects.get(text=word.upper())
        # Si no pasaron levels, usamos los del Word
        lvls = levels_qs if levels_qs is not None else wobj.levels.all()
        names = {lvl.name.lower() for lvl in lvls}
        if "premium" in names:
            score = int(round(score * 1.5))
    except Word.DoesNotExist:
        pass
    return score


def word_fits_board(word: str, board_seed: str) -> bool:
    w = Counter(word.upper())
    b = Counter(board_seed.upper())
    return all(b[c] >= n for c, n in w.items())