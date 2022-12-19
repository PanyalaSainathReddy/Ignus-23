from django.contrib import admin
from .models import Order, Transaction, Pass


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', "amount", "receipt"]


admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction)
admin.site.register(Pass)
