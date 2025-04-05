from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import WordForm
from .models import Category
from . import services


def index(request):
    return HttpResponse("¡Bienvenido a WordShake!")



def game_view(request):
    if request.method == "POST":
        board = request.session.get('board', services.generate_custom_game_board())
    else:
        board = services.generate_custom_game_board()
        request.session['board'] = board  # Guardar en sesión


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
    response = requests.get(url)
    
    if response.status_code == 200:
        Word.objects.create(text=word, is_validated=True)
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

"""def save_score(user_id, word, score):
    word_obj, created = Word.objects.get_or_create(text=word.upper())
    
    data = {
        "user_id": user_id,
        "word": word,
        "points": score,
        "categories": [c.name for c in word_obj.categories.all()],
        "timestamp": datetime.utcnow().isoformat(),
        "date": datetime.utcnow().date().isoformat()
    }
    
    supabase.table("game_score").insert(data).execute()"""
def save_score(user_id, word, score):
    word_obj, created = Word.objects.get_or_create(text=word.upper())
    
    data = {
        "user_id": user_id,
        "word": word,
        "points": score,
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
def generate_board_with_required_letters(words_queryset):
    palabras = [word.text.upper() for word in words_queryset]
    
    if not palabras:
        return generate_board()  # Fallback si no hay palabras

    # Escoge una palabra aleatoria para asegurar que esté presente
    palabra_objetivo = random.choice(palabras)
    letras_requeridas = list(palabra_objetivo)

    # Rellena hasta tener 25 letras
    while len(letras_requeridas) < 25:
        letras_requeridas.append(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    random.shuffle(letras_requeridas)
    return ''.join(letras_requeridas)


def game_view(request):
    try:
        paises = Category.objects.get(name='PAISES')
        nivel1 = Category.objects.get(name='NIVEL 1', parent=paises)
        words_in_category = Word.objects.filter(categories=nivel1)
    except Category.DoesNotExist:
        words_in_category = []
    
    """def generate_custom_game_board():
        letras = ''.join(word.text.upper() for word in words_in_category)
        if len(letras) < 25:
            letras *= (25 // len(letras) + 1)
        return ''.join(random.choice(letras) for _ in range(25))"""
    
    board = board = generate_board_with_required_letters(words_in_category)

    form = WordForm()
    word_valid = None
    score = 0
    user_scores = []
    leaderboard = services.get_leaderboard()

    if request.user.is_authenticated:
        user_scores = services.get_user_scores(request.user.id)

    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word'].upper()
            word_valid = services.check_word_api(word)
            if word_valid:
                score = services.calculate_score(word)
                if request.user.is_authenticated:
                    services.save_score(request.user.id, word, score)
                user_scores = services.get_user_scores(request.user.id)
                leaderboard = services.get_leaderboard()

    return render(request, 'game.html', {
        'board': board,
        'form': form,
        'word_valid': word_valid,
        'score': score,
        'user_scores': user_scores,
        'leaderboard': leaderboard
    })

