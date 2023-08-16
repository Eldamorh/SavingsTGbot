from django.db import models

class User(models.Model):
    chat_id = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)

class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    savings_type = models.CharField(max_length=3, choices=[('EUR', 'EUR'), ('UAH', 'UAH'), ('USD', 'USD')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)