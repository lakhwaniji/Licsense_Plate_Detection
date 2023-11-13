from django.db import models

EVENT = (
    (0, "Entry"),
    (1, "Exit")
)

TYPE = (
    (0, "Employee"),
    (1, "Visitor")
)


class Entry_Exit(models.Model):
    vehicle_number = models.CharField(max_length=80)
    date_created = models.DateTimeField(auto_now_add=True)
    event = models.IntegerField(choices=EVENT, default=0)

    def __str__(self):
        return f"{self.vehicle_number},{self.event}"


class Registered_Vehicles(models.Model):
    vehicle_number = models.CharField(max_length=80, unique=True)
    first = models.CharField(max_length=80)
    uid = models.CharField(max_length=80, unique=True)
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_number},{self.uid}"
