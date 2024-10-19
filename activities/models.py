from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ActivityType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Weightlifting', 'Weightlifting'),
        ('sit-ups', 'sit-ups'),
        ('Swimming', 'Swimming'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False)  # in minutes
    distance = models.DecimalField(max_digits=5, decimal_places=2)  # in km or miles
    calories_burned = models.IntegerField()
    date = models.DateField(null=False, blank=False)
    history = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.activity_type} activity on {self.date}"


class Metrics(models.Model):
    PERIOD_CHOICES = [
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('year', 'Year'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=PERIOD_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_duration = models.IntegerField()  # in minutes
    total_distance = models.DecimalField(max_digits=8, decimal_places=2)  # in km or miles
    total_calories_burned = models.IntegerField()

    class Meta:
        unique_together = ('user', 'period', 'start_date')
        indexes = [
            models.Index(fields=['user', 'period', 'start_date']),
        ]

    def __str__(self):
        return f"{self.user.username}'s metrics for {self.period} starting {self.start_date}"
    



