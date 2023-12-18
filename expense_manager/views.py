from datetime import date

from django.db.models import Q, Sum, F
from django.contrib.auth.forms import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Transaction
from .forms import TransactionForm, TransactionEditForm


@login_required
def index(request):
    if request.user.is_authenticated:
        current_month = date.today().month
        current_year = date.today().year

        total_income = Transaction.objects.filter(
            user=request.user,
            transaction_type='income',
            date__month=current_month,
            date__year=current_year
        ).aggregate(Sum('amount'))['amount__sum']

        total_expense = Transaction.objects.filter(
            user=request.user,
            transaction_type='expense',
            date__month=current_month,
            date__year=current_year
        ).aggregate(Sum('amount'))['amount__sum']

        expenses_by_category = Transaction.objects.filter(
            user=request.user,
            transaction_type='expense',
            date__month=current_month,
            date__year=current_year
        ).values('category__category_name').annotate(total_amount=Sum('amount'))

        incomes_by_category = Transaction.objects.filter(
            user=request.user,
            transaction_type='income',
            date__month=current_month,
            date__year=current_year
        ).values('category__category_name').annotate(total_amount=Sum('amount'))

        context = {
            'total_income': total_income,
            'total_expense': total_expense,
            'current_month': current_month,
            'current_year': current_year,
            'expenses_by_category': expenses_by_category,
            'incomes_by_category': incomes_by_category,
        }
        return render(request, 'index.html', context)


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-id')
    query = request.GET.get('q')
    if query:
        transactions = transactions.filter(
            Q(transaction_type__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(amount__icontains=query) |
            Q(description__icontains=query) |
            Q(date__icontains=query)
        )
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    context = {
        'transactions': transactions,
        'query': query,
    }
    return render(request, 'transaction_list.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(user=request.user, data=request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'add_transaction.html', {'form': form})


@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    return render(request, 'transaction_detail.html', {'transaction': transaction})


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        form = TransactionEditForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_detail', transaction_id=transaction.id)
    else:
        form = TransactionEditForm(instance=transaction)
    return render(request, 'transaction_edit.html', {'form': form, 'transaction': transaction})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if transaction.user == request.user:
        transaction.delete()
    return redirect('transaction_list')


@login_required
def expense_summary(request):
    current_year = timezone.now().year
    start_date = f'{current_year}-01-01'
    end_date = f'{current_year}-12-31'
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
    expenses = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__range=[start_date, end_date]
    ).order_by('-date', '-id')
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum']
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    expenses = paginator.get_page(page_number)
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'expense_summary.html', context)


@login_required
def income_summary(request):
    current_year = timezone.now().year
    start_date = f'{current_year}-01-01'
    end_date = f'{current_year}-12-31'
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
    income = Transaction.objects.filter(
        user=request.user,
        transaction_type='income',
        date__range=[start_date, end_date]
    ).order_by('-date', '-id')
    total_income = income.aggregate(Sum('amount'))['amount__sum']
    paginator = Paginator(income, 10)
    page_number = request.GET.get('page')
    income = paginator.get_page(page_number)
    context = {
        'income': income,
        'total_income': total_income,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'income_summary.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'An account with email {email} has already been registered!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} has been registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('register')
    return render(request, 'register.html')