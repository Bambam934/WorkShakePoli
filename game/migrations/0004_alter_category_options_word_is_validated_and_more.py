# Generated by Django 5.1.7 on 2025-04-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_category_level_category_lft_category_rght_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.AddField(
            model_name='word',
            name='is_validated',
            field=models.BooleanField(default=False, verbose_name='¿Validada?'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('parent', 'name')},
        ),
    ]
