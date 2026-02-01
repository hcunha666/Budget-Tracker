from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from .models import Transaction, Category
from .forms import TransactionForm
import datetime

def home(request):
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    
    # Calculate stats
    total_income = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    
    monthly_income = Transaction.objects.filter(type='income', date__gte=first_day_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_expense = Transaction.objects.filter(type='expense', date__gte=first_day_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    
    recent_transactions = Transaction.objects.select_related('category').order_by('-date', '-created_at')[:10]
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TransactionForm()
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'recent_transactions': recent_transactions,
        'form': form,
        'current_month': today.strftime('%B %Y'),
    }
    return render(request, 'core/index.html', context)