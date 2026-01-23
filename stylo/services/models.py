from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.PositiveBigIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.name

class Stylist(models.Model):
    name = models.CharField(max_length=100)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name

class WorkingHour(models.Model):

    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(
        choices=[
            (0, 'Monday'),(1, 'Tuesday'),(2, 'Wednesday'),(3, 'Thursday'),(4, 'Friday'),(5, 'Saturday'),(6, 'Sunday')
        ]
    )

    start_time = models.TimeField()
    end_time = models.TimeField()


class Break(models.Model):
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    