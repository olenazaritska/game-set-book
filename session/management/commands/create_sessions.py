from django.core.management.base import BaseCommand
from session.models import WorkingHours, Session
from datetime import datetime, timedelta, time
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Create sessions for courts based on sport club working hours for the next 7 days."

    def handle(self, *args, **kwargs):
        today = datetime.today().date()

        for i in range(7):
            day = today + timedelta(days=i)
            day_of_week = day.weekday()

            working_hours = WorkingHours.objects.filter(day_of_week=day_of_week)

            for wh in working_hours:
                sport_club = wh.sport_club
                opening_time = wh.opening_at
                closing_time = wh.closing_at

                if not opening_time or not closing_time:
                    self.stdout.write(
                        f"{sport_club.name} is closed on {day.strftime('%A')}. Skipping session creation."
                    )
                    continue

                if Session.objects.filter(
                    date=day, court__sport_club=sport_club
                ).exists():
                    self.stdout.write(
                        f"Sessions already exist for {sport_club.name} on {day.strftime('%A')}. Skipping."
                    )
                    continue

                courts = sport_club.courts.all()
                current_time = opening_time

                while current_time < closing_time:
                    for court in courts:
                        start_time = current_time
                        end_time = time(current_time.hour + 1, current_time.minute)

                        try:
                            Session.objects.create(
                                court=court,
                                date=day,
                                start_time=start_time,
                                end_time=end_time,
                            )
                            self.stdout.write(
                                f"Created session for {court.sport_club.name} "
                                f"Court {court.number} "
                                f"on {day.strftime('%A')} "
                                f"from {start_time} to {end_time}."
                            )
                        except IntegrityError:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Session for Court {court.number} "
                                    f"on {day} "
                                    f"from {start_time} to {end_time} already exists."
                                )
                            )
                            continue

                    current_time = time(current_time.hour + 1, current_time.minute)

        self.stdout.write(
            self.style.SUCCESS(
                "Sessions created successfully or skipped if they already existed."
            )
        )
