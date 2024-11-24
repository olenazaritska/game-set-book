from celery import shared_task
from datetime import datetime, timedelta, time
from django.db.utils import IntegrityError
from .models import Session, WorkingHours


@shared_task
def create_sessions_for_the_same_day_next_week():
    today = datetime.now().date()
    next_week_day = today + timedelta(days=7)
    current_weekday = today.weekday()

    working_hours = WorkingHours.objects.filter(day_of_week=current_weekday)

    for wh in working_hours:
        sport_club = wh.sport_club
        opening_time = wh.opening_at
        closing_time = wh.closing_at

        if not opening_time or not closing_time:
            continue

        if Session.objects.filter(
            date=next_week_day, court__sport_club=sport_club
        ).exists():
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
                        date=next_week_day,
                        start_time=start_time,
                        end_time=end_time,
                    )
                except IntegrityError:
                    continue

            current_time = time(current_time.hour + 1, current_time.minute)
