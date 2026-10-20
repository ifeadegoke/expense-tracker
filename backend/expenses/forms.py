from django import forms
from .models import Expense, Budget


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount']