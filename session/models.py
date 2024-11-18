from django.db import models


class SportClub(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=250)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_sport_club")
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    sport_club = models.ForeignKey(
        SportClub, on_delete=models.CASCADE, related_name="working_hours"
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    opening_at = models.TimeField(null=True, blank=True)
    closing_at = models.TimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sport_club", "day_of_week"], name="unique_working_day"
            )
        ]
        ordering = ["sport_club", "day_of_week"]

    def __str__(self):
        return (
            f"({self.sport_club.name}) "
            f"{self.get_day_of_week_display()} "
            f"{self.opening_at}-{self.closing_at}"
        )
