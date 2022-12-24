from django.contrib import admin
from .models import Order, Transaction, Pass


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', "amount", "user", "receipt"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['payment_id', "order", "amount", "user", "status"]


class PassAdmin(admin.ModelAdmin):
    list_display = ['name', "amount", "type"]


admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Pass, PassAdmin)
