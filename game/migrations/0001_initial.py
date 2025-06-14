# Generated by Django 5.2 on 2025-04-28 04:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categorias', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('points', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50, unique=True, verbose_name='Palabra')),
                ('is_from_api', models.BooleanField(default=False, verbose_name='De la API')),
                ('is_validated', models.BooleanField(default=False, verbose_name='¿Validada?')),
                ('levels', models.ManyToManyField(blank=True, related_name='words', to='categorias.level', verbose_name='Niveles')),
            ],
            options={
                'verbose_name': 'Palabra',
                'verbose_name_plural': 'Palabras',
                'ordering': ['text'],
            },
        ),
    ]
