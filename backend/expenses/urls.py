from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('delete/<int:expense_id>/', views.expense_delete, name='expense_delete'),
    
]