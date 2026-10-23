from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings




class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Data', 'Data'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other')
    ]

    category = models.CharField(max_length = 20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.description} - {self.amount}"
    
class Budget(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return f"Budget: {self.amount}"

        