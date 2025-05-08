# categorias/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Level
from perfil.models import UserProfile

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
    user_neon_color = '#00ffcc' 

    if request.user.is_authenticated:
        try:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            if profile.neon_color: 
                user_neon_color = profile.neon_color
                print(user_neon_color)
            else:
                user_neon_color = UserProfile._meta.get_field('neon_color').default

        except UserProfile.DoesNotExist:
            user_neon_color = UserProfile._meta.get_field('neon_color').default
        except Exception as e:
            try:
                user_neon_color = UserProfile._meta.get_field('neon_color').default
            except Exception as e_default:
                user_neon_color = '#00ffcc' # Último recurso
        context = {
        'categories': categories,
        'levels_by_category': levels_by_category,
        'neon_color':       user_neon_color, # Esta es la clave que usa tu game.html
        }
    return render(request, 'categorias/select_level.html', context)


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
