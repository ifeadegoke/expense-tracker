from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views, api

router = DefaultRouter()
router.register('expenses', api.ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('delete/<int:expense_id>/', views.expense_delete, name='expense_delete'),
    path('edit/<int:expense_id>/', views.expense_edit, name = 'expense_edit'),
    path('budget/', views.set_budget, name='set_budget'),
    path('signup/', views.signup, name='signup'),
    path('api/', include(router.urls)),
    path('profile/', views.profile, name='profile'),
    path('profile/password/', views.ChangePasswordView.as_view(), name='change_password'),
    
]