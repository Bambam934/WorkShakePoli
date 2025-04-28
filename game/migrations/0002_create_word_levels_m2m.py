from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
        ('categorias', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS game_word_levels (
                id        SERIAL PRIMARY KEY,
                word_id   INTEGER NOT NULL
                          REFERENCES game_word(id)
                          ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
                level_id  INTEGER NOT NULL
                          REFERENCES categorias_level(id)
                          ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
            );
            CREATE UNIQUE INDEX IF NOT EXISTS
                game_word_levels_word_id_level_id_uniq
                ON game_word_levels(word_id, level_id);
            """,
            reverse_sql="""
            DROP TABLE IF EXISTS game_word_levels CASCADE;
            """,
        ),
    ]
