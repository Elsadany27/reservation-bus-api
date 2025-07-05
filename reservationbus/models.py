from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # ❌ No create_superuser method at all


class User(AbstractBaseUser):
    email = models.EmailField(unique=True,null=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


#trips
import random
from django.db import models
from datetime import datetime

class Trip(models.Model):
    from_area = models.CharField(max_length=100)
    to_area = models.CharField(max_length=100)
    time_of_travel = models.CharField(max_length=50)   # e.g. "08:00"
    time_of_reach = models.CharField(max_length=50,null=True)    # e.g. "10:30"
    duration = models.CharField(max_length=50, blank=True, null=True)  # auto-filled
    price = models.CharField(max_length=20)
    date = models.CharField(max_length=20)

    driver_name = models.CharField(max_length=100, blank=True, null=True)
    trip_number = models.IntegerField(blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        # Assign random trip number
        if not self.trip_number:
            while True:
                random_number = random.randint(1, 999)
                if not Trip.objects.filter(trip_number=random_number).exists():
                    self.trip_number = random_number
                    break

        # Calculate duration if times are valid
        try:
            t1 = datetime.strptime(self.time_of_travel, "%H:%M")
            t2 = datetime.strptime(self.time_of_reach, "%H:%M")
            if t2 < t1:  # crossing midnight
                t2 = t2.replace(day=t2.day + 1)
            delta = t2 - t1
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60
            self.duration = f"{hours}h {minutes}m"
        except Exception:
            self.duration = "Invalid time"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_area} to {self.to_area} on {self.date} (#{self.trip_number})"


class Ticket(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tickets')
    passenger_name = models.CharField(max_length=100)
    seat_number = models.PositiveIntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.passenger_name} - Seat {self.seat_number}"
