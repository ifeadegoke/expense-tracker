from django.db import models

# Create your models here.

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Data', 'Data'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other')
    ]

    category = models.CharField(max_length = 20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.description} - {self.amount}"
    
