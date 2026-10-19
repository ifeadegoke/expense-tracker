from django.shortcuts import render
from .models import Expense

def expense_list(request):
    expenses = Expense.objects.all()
    total = sum(e.amount for e in expenses)
    context ={
        'expenses': expenses,
        'total': total,
    }
    return render(request, 'expenses/expense_list.html', context)


