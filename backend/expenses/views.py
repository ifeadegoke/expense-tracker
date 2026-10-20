from django.shortcuts import render, redirect, get_object_or_404
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
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
    return redirect('expense_list')


