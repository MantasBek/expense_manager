from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    CATEGORY_CHOICES = (
        ('a', 'Housing'),
        ('b', 'Transportation'),
        ('c', 'Food'),
        ('d', 'Utilities'),
        ('e', 'Clothing'),
        ('f', 'Medical/Healthcare'),
        ('g', 'Insurance'),
        ('h', 'Household Items/Supplies'),
        ('i', 'Personal'),
        ('j', 'Debt'),
        ('k', 'Retirement'),
        ('l', 'Education'),
        ('m', 'Savings'),
        ('n', 'Gifts/Donations'),
        ('r', 'Entertainment'),
        ('o', 'Other')
    )

    category_name = models.CharField(max_length=1, choices=CATEGORY_CHOICES, blank=True, null=True,
                                     help_text='Categories')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.get_category_name_display()


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=50, null=True, blank=True)
    date = models.DateField()

    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return self.user.username