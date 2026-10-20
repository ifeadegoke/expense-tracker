from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm

def expense_list(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    expenses = Expense.objects.all()
    total = sum(e.amount for e in expenses)
    context = {
        'expenses': expenses,
        'total': total,
        'form': form,
    }
    return render(request, 'expenses/expense_list.html', context)