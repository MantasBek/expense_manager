from django.contrib import admin
from .models import Transaction, UserProfile, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'user')
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UserProfile)
admin.site.register(Category, CategoryAdmin)

