from django.db import models

# Create your models here.

class Payment(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    account_number = models.CharField(max_length=100)
    transaction_time = models.DateTimeField()
