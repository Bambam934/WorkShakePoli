# Generated by Django 5.2 on 2025-04-05 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_category_level_category_lft_category_rght_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
    ]
