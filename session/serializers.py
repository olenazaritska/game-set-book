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
        fields = ("id", "name", "location", "working_hours")
