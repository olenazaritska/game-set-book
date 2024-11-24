from django.core.management.base import BaseCommand
from django.core.management import call_command
from session.models import SportClub, WorkingHours, Court


class Command(BaseCommand):
    help = "Load initial data for sport clubs, working hours & courts if not already present"

    def handle(self, *args, **kwargs):
        if not SportClub.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("No SportClub data found, loading fixtures...")
            )
            call_command("loaddata", "fixtures/sport_clubs.json")
        else:
            self.stdout.write(
                self.style.SUCCESS("SportClub data already exists, skipping...")
            )

        if not WorkingHours.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("No WorkingHours data found, loading fixtures...")
            )
            call_command("loaddata", "fixtures/working_hours.json")
        else:
            self.stdout.write(
                self.style.SUCCESS("WorkingHours data already exists, skipping...")
            )

        if not Court.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("No Court data found, loading fixtures...")
            )
            call_command("loaddata", "fixtures/courts.json")
        else:
            self.stdout.write(
                self.style.SUCCESS("Court data already exists, skipping...")
            )
