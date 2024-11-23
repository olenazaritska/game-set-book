from rest_framework import serializers

from session.models import WorkingHours, SportClub


class WorkingHoursSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = WorkingHours
        fields = ("day", "time")

    def get_day(self, obj):
        return obj.get_day_of_week_display()

    def get_time(self, obj):
        if obj.opening_at and obj.closing_at:
            return (
                f"{obj.opening_at.strftime('%H:%M')}-{obj.closing_at.strftime('%H:%M')}"
            )
        return "Closed"


class SportClubSerializer(serializers.ModelSerializer):
    working_hours = WorkingHoursSerializer(many=True)

    class Meta:
        model = SportClub
        fields = ("id", "name", "location", "logo", "working_hours")


class SportClubSessionsSerializer(serializers.ModelSerializer):
    sport_club_id = serializers.IntegerField(source="id")
    sport_club_name = serializers.CharField(source="name")
    sessions_by_date = serializers.SerializerMethodField()

    class Meta:
        model = SportClub
        fields = ("sport_club_id", "sport_club_name", "sessions_by_date")

    def get_sessions_by_date(self, obj):
        courts = obj.courts.all()
        sessions_by_date = {}

        for court in courts:
            for session in court.filtered_sessions:
                date = session.date.strftime("%Y-%m-%d")
                if date not in sessions_by_date:
                    sessions_by_date[date] = {}

                court_number = f"court #{court.number}"
                if court_number not in sessions_by_date[date]:
                    sessions_by_date[date][court_number] = {
                        "surface": court.surface,
                        "court_type": court.court_type,
                        "game_type": court.game_type,
                        "sessions": [],
                    }

                sessions_by_date[date][court_number]["sessions"].append(
                    {
                        "id": session.id,
                        "time_slot": f"{session.start_time.strftime('%H:%M')}-{session.end_time.strftime('%H:%M')}",
                        "booked": session.booked,
                    }
                )

        return sessions_by_date
