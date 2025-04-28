# game/migrations/0004_word_is_validated_alter_word_categories_and_more.py

# Importa SeparateDatabaseAndState si no está ya importado
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0001_initial'),
        ('game', '0003_category_level_category_lft_category_rght_and_more'),
    ]

    operations = [

        migrations.AlterField(
            model_name='word',
            name='categories',
            field=models.ManyToManyField(to='categorias.category', verbose_name='Categorías'),
        ),
    ]