from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from django.contrib import messages
from .models import Category, Word
import requests



"""@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('categories',)"""
class WordInline(admin.TabularInline):
    model = Word.categories.through  # M2M intermedia
    extra = 1

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    inlines = [WordInline]
    list_display = ('name', 'parent')

def validar_palabra(palabra):
    """Función helper para validar palabras con la API"""
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{palabra}", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def importar_palabras_desde_datamuse(modeladmin, request, queryset):
    """Acción administrativa para importar palabras desde DataMuse"""
    url = "https://api.datamuse.com/words?sp=?????&max=50"
    
    try:
        response = requests.get(url)
        data = response.json()
        contador = 0
        
        for item in data:
            palabra = item['word'].lower().strip()
            if len(palabra) < 3:  # Ignorar palabras muy cortas
                continue
                
            if validar_palabra(palabra):
                _, created = Word.objects.get_or_create(text=palabra)
                if created:
                    contador += 1
                    
        messages.success(request, f"{contador} palabras válidas importadas de {len(data)} obtenidas")
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_from_api', 'es_valida')
    search_fields = ('text',)
    filter_horizontal = ('categories',)
    actions = [importar_palabras_desde_datamuse]

    def es_valida(self, obj):
        """Método para mostrar el estado de validación en el admin"""
        return validar_palabra(obj.text)
    es_valida.boolean = True
    es_valida.short_description = 'Válida'