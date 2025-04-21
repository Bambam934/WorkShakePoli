# categorias/migrations/0001_initial.py

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        # ¡Quita SeparateDatabaseAndState! Deja CreateModel directamente.
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='categorias.category', verbose_name='Categoría padre')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                # ¡Ya no especificamos db_table aquí tampoco!
                'unique_together': {('parent', 'name')},
            },
        ),
        # ¡Asegúrate que no quede el SeparateDatabaseAndState envolviendo esto!
    ]