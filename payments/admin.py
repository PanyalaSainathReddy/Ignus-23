from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from .models import Order, Transaction, PromoCode


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'pay_for', 'amount', 'currency', 'request_timestamp', 'response_timestamp', 'result_code', 'result_msg', 'transaction_token', 'user__registration_code', 'user__user__first_name', 'user__user__last_name')


class OrderAdmin(ImportExportActionModelAdmin):
    resource_class = OrderResource
    list_display = ['id', "amount", "user", 'pay_for', 'transacted', 'transaction_status']
    list_filter = ['pay_for']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__registration_code']


class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('txn_id', 'bank_txn_id', 'status', 'order__id', 'amount', 'gateway_name', 'payment_mode', 'resp_code', 'resp_msg', 'timestamp', 'user__registration_code', 'user__user__first_name', 'user__user__last_name')


class TransactionAdmin(ImportExportActionModelAdmin):
    resource_class = TransactionResource
    list_display = ['txn_id', "order", "amount", "user", "status"]
    list_filter = ['status']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__registration_code', 'status', 'order__id', 'txn_id']


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'uses', 'max_uses', 'pass_name', 'discounted_amount', 'valid']
    list_filter = ['valid']
    search_fields = ['code', 'pass_name', 'discounted_amount']


admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
