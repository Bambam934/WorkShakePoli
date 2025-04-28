import random
import requests
from datetime import datetime
from django.core.cache import cache
from django.conf import settings
from categorias.models import Category, Level
from .models import Word
import logging


supabase = settings.SUPABASE_CLIENT

LETTER_POINTS = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
    'I': 1, 'J': 8, 'K': 8, 'L': 1, 'M': 3, 'N': 1, '\u00d1': 8, 'O': 1,
    'P': 3, 'Q': 5, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 10,
    'X': 8, 'Y': 4, 'Z': 10
}


def generate_board():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(random.choice(letters) for _ in range(25))


def generate_custom_game_board(categoria_id,nivelC):
    try:
        categoria = Category.objects.get(name=categoria_id)
        nivel = Category.objects.get(name=nivelC, parent=categoria)
        words_in_category = Word.objects.filter(categories=nivel)
        diccionario = list(words_in_category.values_list("text", flat=True))
    except Category.DoesNotExist:
        words_in_category = []

    if words_in_category.exists():
        return generate_board_with_required_letters(diccionario)
    else:
        return generate_board()




logger = logging.getLogger(__name__)
def generate_board_with_required_letters(words_queryset):
    palabras = [word.text.upper() for word in words_queryset]

    if not palabras:
        return generate_board()

    # Seleccionamos al azar 5 palabras (o menos si no hay suficientes)
    random.shuffle(palabras)
    palabras_seleccionadas = palabras[:5]

    letras_requeridas = []
    for palabra in palabras_seleccionadas:
        letras_requeridas.extend(list(palabra))

    # Completamos con letras al azar si faltan para llegar a 25
    while len(letras_requeridas) < 25:
        letras_requeridas.append(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    random.shuffle(letras_requeridas)
    return ''.join(letras_requeridas)


def check_word_api(word):
    word = word.upper()
    cache_key = f'word_validation_{word}'
    cached_result = cache.get(cache_key)
    
    if cached_result is not None:
        return cached_result

    try:
        word_obj = Word.objects.get(text=word)
        cache.set(cache_key, word_obj.is_validated, 86400)
        return word_obj.is_validated
    except Word.DoesNotExist:
        pass

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        logger.error(f"Error consultando API externa: {e}")
        return False  # No se pudo validar

    if response.status_code == 200:
        Word.objects.create(text=word, is_validated=True, is_from_api=True)
        cache.set(cache_key, True, 86400)
        return True

    cache.set(cache_key, False, 86400)
    return False

def calculate_score(word):
    try:
        word_obj = Word.objects.get(text=word.upper())
        multiplier = 1.5 if any(category.name == 'Premium' for category in word_obj.categories.all()) else 1
    except Word.DoesNotExist:
        multiplier = 1

    base_score = sum(LETTER_POINTS.get(letter, 0) for letter in word.upper())
    return int(base_score * multiplier)


def save_score(user_id, word, score):
    word_obj, created = Word.objects.get_or_create(text=word.upper())

    data = {
        "user_id": user_id,
        "word": word,
        "points": score,
        "categories": [c.name for c in word_obj.categories.all()],
        "timestamp": datetime.utcnow().isoformat(),
        "date": datetime.utcnow().date().isoformat()
    }

    supabase.table("game_score").insert(data).execute()


def get_user_scores(user_id):
    response = supabase.table("game_score") \
        .select("word, points, date") \
        .eq("user_id", user_id) \
        .order("date", desc=True) \
        .limit(5) \
        .execute()
    return response.data if response.data else []


def get_leaderboard():
    response = supabase.rpc("get_leaderboard").execute()
    return response.data if response.data else []


def generate_custom_game_board(categoria_name, nivel_name):
    """
    Genera un tablero obligando a incluir letras de palabras
    del nivel indicado.  Si el nivel no tiene palabras, genera
    un tablero aleatorio.
    """
    try:
        categoria = Category.objects.get(name=categoria_name)
        nivel     = Level.objects.get(name=nivel_name, category=categoria)
        words_in_level = Word.objects.filter(levels=nivel)
    except (Category.DoesNotExist, Level.DoesNotExist):
        words_in_level = Word.objects.none()

    if words_in_level.exists():
        return generate_board_with_required_letters(words_in_level)
    return generate_board()