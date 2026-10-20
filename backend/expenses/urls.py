from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('delete/<int:expense_id>/', views.expense_delete, name='expense_delete'),
    path('edit/<int:expense_id>/', views.expense_edit, name = 'expense_edit'),
    path('budget/', views.set_budget, name='set_budget'),
    
    
]