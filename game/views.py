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

