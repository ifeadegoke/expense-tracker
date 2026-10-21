from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Budget
from .forms import ExpenseForm, BudgetForm
from django.db.models import Sum

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

    category_data =(
        Expense.objects
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by("category")
    )

    chart_labels = [item['category'] for item in category_data]
    chart_values = [float(item['total']) for item in category_data]

    budget = Budget.objects.first()
    budget_form = BudgetForm(instance=budget)
    remaining = None
    percentage = None
    status = None

    if budget:
        remaining = budget.amount - total
        percentage = (total / budget.amount) * 100
        if percentage >= 100:
            status = 'over'
        elif percentage >= 80:
            status = 'warning'
        else:
            status = 'ok'

    context = {
        'expenses': expenses,
        'total': total,
        'form': form,
        'budget': budget,
        'budget_form': budget_form,
        'remaining': remaining,
        'percentage': percentage,
        'status': status, 
        'chart_labels' : chart_labels,
        'chart_values' : chart_values,
        
    }
    return render(request, 'expenses/expense_list.html', context)

    
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
    return redirect('expense_list')


def expense_edit(request, expense_id):
    expense = get_object_or_404(Expense, id = expense_id)
    if request.method =='POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
            form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_edit.html', {'form':form, 'expense': expense})


def set_budget(request):
    if request.method =='POST':
        budget = Budget.objects.first()
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
    return redirect('expense_list')
    
    