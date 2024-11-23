from django.db import models


class SportClub(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    logo = models.ImageField(upload_to="sport_clubs/", blank=True, null=True)

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


class Court(models.Model):
    SURFACE_CHOICES = [
        ("CLAY", "Clay"),
        ("HARD", "Hard"),
        ("GRASS", "Grass"),
        ("OTHER", "Other"),
    ]

    COURT_TYPE_CHOICES = [
        ("INDOOR", "Indoor"),
        ("OUTDOOR", "Outdoor"),
    ]

    sport_club = models.ForeignKey(
        SportClub, on_delete=models.CASCADE, related_name="courts"
    )
    number = models.PositiveSmallIntegerField()
    surface = models.CharField(
        max_length=100,
        choices=SURFACE_CHOICES,
    )
    court_type = models.CharField(
        max_length=100,
        choices=COURT_TYPE_CHOICES,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sport_club", "number"], name="unique_court"
            )
        ]
        ordering = ["sport_club", "number"]

    def __str__(self):
        return f"{self.sport_club.name} court {self.number} ({self.surface})"


class Session(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["court", "date", "start_time"], name="unique_session"
            )
        ]
        ordering = ["court", "date", "start_time"]

    def __str__(self):
        return (
            f"({self.court.sport_club.name} {self.court.number}) "
            f"{self.date} {self.start_time}-{self.end_time}"
        )
