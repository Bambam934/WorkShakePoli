# Generated by Django 5.2 on 2025-05-12 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0002_userprofile_neon_color_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='total_score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_words',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
