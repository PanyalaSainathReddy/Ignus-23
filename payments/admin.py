from django.contrib import admin

from .models import Order, Transaction


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', "amount", "user", 'pay_for', 'transacted', 'transaction_status']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['txn_id', "order", "amount", "user", "status"]


admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
