# Generated by Django 5.2 on 2025-05-12 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0002_skin'),
        ('perfil', '0004_userprofile_coins'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active_skin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='achievements.skin'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='owned_skins',
            field=models.ManyToManyField(blank=True, related_name='owners', to='achievements.skin'),
        ),
    ]
