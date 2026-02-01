from django.db import models
from django.utils import timezone

class Category(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='expense')
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="FontAwesome icon name (e.g., fa-utensils)")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=TYPES, default='expense')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} - {self.description[:20]}"