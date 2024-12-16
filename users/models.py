
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null = True, blank = True)


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(max_length=50, default='Basic')  # e.g., 'Basic', 'Premium'
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan_name} (Active: {self.active})"