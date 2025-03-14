import requests
import random
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from .forms import WordForm
from django.http import HttpResponse

def index(request):
    return HttpResponse("\u00a1Bienvenido a WordShake!")

# Obtener cliente de Supabase
supabase = settings.SUPABASE_CLIENT

# Puntos por letra
LETTER_POINTS = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
    'I': 1, 'J': 8, 'K': 8, 'L': 1, 'M': 3, 'N': 1, '\u00d1': 8, 'O': 1,
    'P': 3, 'Q': 5, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 10,
    'X': 8, 'Y': 4, 'Z': 10
}

# Generar letras aleatorias para el tablero
def generate_letters():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return random.sample(letters, 7)

# Verificar palabra usando API externa
def check_word_api(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
    response = requests.get(url)
    return response.status_code == 200  # Si la API responde con 200, la palabra es válida

# Calcular la puntuación de una palabra
def calculate_score(word):
    return sum(LETTER_POINTS.get(letter, 0) for letter in word)

# Guardar puntuación en Supabase


def save_score(user_id, word, score):
    data = {
        "user_id": user_id,
        "word": word,
        "points": score,
        "timestamp": datetime.utcnow().isoformat(),  # Timestamp válido
        "date": datetime.utcnow().date().isoformat()  # Fecha sin hora
    }

    supabase.table("game_score").insert(data).execute()



# Obtener historial de puntuaciones de un usuario
def get_user_scores(user_id):
    response = supabase.table("game_score") \
        .select("word, points, date") \
        .eq("user_id", user_id) \
        .order("date", desc=True) \
        .limit(5) \
        .execute()

    return response.data if response.data else []

# Obtener ranking de jugadores con más puntos acumulados
def get_leaderboard():
    response = supabase.rpc("get_leaderboard").execute()  # Llamamos a la función SQL

    if not response.data:
        return []

    print("Leaderboard data:", response.data)  # Debug para ver qué retorna Supabase
    return response.data

# Vista principal del juego
def game_view(request):
    letters = generate_letters()
    form = WordForm()
    word_valid = None
    score = 0
    user_scores = []
    leaderboard = get_leaderboard()

    if request.user.is_authenticated:
        user_scores = get_user_scores(request.user.id)

    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word'].upper()
            word_valid = check_word_api(word)  # Verificar con API
            if word_valid:
                score = calculate_score(word)
                if request.user.is_authenticated:
                    save_score(request.user.id, word, score)
                user_scores = get_user_scores(request.user.id)
                leaderboard = get_leaderboard()

    return render(request, 'game.html', {
        'letters': letters,
        'form': form,
        'word_valid': word_valid,
        'score': score,
        'user_scores': user_scores,
        'leaderboard': leaderboard
    })