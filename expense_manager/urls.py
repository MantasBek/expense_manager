# expense_manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('register/', views.register, name='register'),
    path('transactions/<int:transaction_id>', views.transaction_detail, name='transaction_detail'),
    path('transactions/<int:transaction_id>/edit', views.edit_transaction, name='edit_transaction'),
    path('expense_summary/', views.expense_summary, name='expense_summary'),
    path('income_summary/', views.income_summary, name='income_summary'),
    path('transactions/<int:transaction_id>/delete', views.delete_transaction, name='delete_transaction'),
]