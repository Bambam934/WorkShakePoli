from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Sembrar logros y desafíos desde initial_achievements.json"

    def handle(self, *args, **options):
        # Esto carga el fixture con get_or_create internamente:
        self.stdout.write("Cargando fixture achievements/fixtures/initial_achievements.json…")
        call_command('loaddata', 'initial_achievements.json', verbosity=1)
        self.stdout.write(self.style.SUCCESS("✅ Logros y desafíos sembrados."))