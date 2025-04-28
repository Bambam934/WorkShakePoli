# categorias/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Level


@login_required
def select_level_view(request):
    """
    Muestra el formulario de selección Categoría → Nivel y envía
    al usuario a la partida cuando elige ambos valores.
    """
    categories = Category.objects.prefetch_related('levels').order_by('name')

    levels_by_category = {
        cat.name: [
            lvl.name for lvl in sorted(cat.levels.all(),
                                       key=lambda x: (x.order, x.name))
        ]
        for cat in categories
    }

    # Si llegan datos vía GET, redirigimos directamente al juego
    cat_name = request.GET.get('categoria_name')
    lvl_name = request.GET.get('nivel')
    if cat_name and lvl_name:
        return redirect('game:play',
                        categoria_name=cat_name,
                        nivel_name=lvl_name)

    return render(
        request,
        'categorias/select_level.html',
        {
            'categories': categories,
            'levels_by_category': levels_by_category,
        }
    )


@login_required
def start_game_view(request):
    """
    Valida la pareja categoría-nivel y redirige a game:play.
    Se invoca desde el formulario de selección (método GET).
    """
    categoria_name = request.GET.get('categoria_name')
    nivel_name     = request.GET.get('nivel')

    if not categoria_name or not nivel_name:
        messages.error(request, 'Debes seleccionar una categoría y un nivel.')
        return redirect('categorias:select_level')

    try:
        cat = Category.objects.get(name=categoria_name)
        Level.objects.get(name=nivel_name, category=cat)
    except (Category.DoesNotExist, Level.DoesNotExist):
        messages.error(
            request,
            f'La categoría “{categoria_name}” o el nivel “{nivel_name}” no existen.'
        )
        return redirect('categorias:select_level')

    return redirect('game:play',
                    categoria_name=categoria_name,
                    nivel_name=nivel_name)
