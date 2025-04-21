# game/migrations/0004_word_is_validated_alter_word_categories_and_more.py

# Importa SeparateDatabaseAndState si no está ya importado
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0001_initial'),
        ('game', '0003_category_level_category_lft_category_rght_and_more'),
    ]

    operations = [
        # La operación AddField podría estar ya envuelta así por un paso anterior:
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='word',
                    name='is_validated',
                    field=models.BooleanField(default=False, verbose_name='¿Validada?'),
                ),
            ],
            database_operations=[],
        ),

        # Esta operación SÍ necesita tocar la base de datos (ALTER TABLE)
        # para actualizar la relación ManyToMany, así que NO la envuelvas.
        migrations.AlterField(
            model_name='word',
            name='categories',
            field=models.ManyToManyField(to='categorias.category', verbose_name='Categorías'),
        ),

        # ¡Envuelve SOLO DeleteModel con SeparateDatabaseAndState!
        migrations.SeparateDatabaseAndState(
            # Operación de Estado: Elimina Category del estado de la app 'game'
            state_operations=[
                migrations.DeleteModel(
                    name='Category',
                ),
            ],
            # Operación de Base de Datos: No hacer NADA (no intentar DROP TABLE)
            database_operations=[],
        )
    ]