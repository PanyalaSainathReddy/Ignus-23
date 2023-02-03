from django.contrib import admin

from .models import Order, Transaction


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', "amount", "user", 'pay_for', 'transacted', 'transaction_status']
    list_filter = ['pay_for']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__registration_code']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['txn_id', "order", "amount", "user", "status"]
    list_filter = ['status']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__registration_code', 'status', 'order', 'txn_id']


admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
