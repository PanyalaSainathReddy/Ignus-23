from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from .models import Order, Transaction, PromoCode


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'pay_for', 'amount', 'currency', 'request_timestamp', 'response_timestamp', 'result_code', 'result_msg', 'transaction_token', 'user__registration_code', 'user__user__first_name', 'user__user__last_name')


class OrderTransactedFilter(admin.SimpleListFilter):
    title = 'Filter By Transacted'
    parameter_name = 'transacted'

    def lookups(self, request, model_admin):
        return (
            ('True', 'True'),
            ('False', 'False'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            new_queryset = []
            for query in queryset.all():
                print(query)
                print(query.transaction_set)
                if query.transaction_set.count() == 1:
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == 'False':
            new_queryset = []
            for query in queryset.all():
                print(query)
                print(query.transaction_set)
                if query.transaction_set.count() == 0:
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset


class OrderTransactionStatusFilter(admin.SimpleListFilter):
    title = 'Filter By Transaction Status'
    parameter_name = 'transaction_status'

    def lookups(self, request, model_admin):
        return (
            ('TXN_SUCCESS', 'TXN_SUCCESS'),
            ('TXN_FAILURE', 'TXN_FAILURE'),
            ('PENDING', 'PENDING')
        )

    def queryset(self, request, queryset):
        if self.value() == "TXN_SUCCESS":
            new_queryset = []
            for query in queryset.all():
                if query.transaction_set.first().status == self.value():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == "TXN_FAILURE":
            new_queryset = []
            for query in queryset.all():
                if query.transaction_set.first().status == self.value():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == "PENDING":
            new_queryset = []
            for query in queryset.all():
                if query.transaction_set.first().status == self.value():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset


class OrderIsRandomFilter(admin.SimpleListFilter):
    title = 'Filter By Is Random'
    parameter_name = 'is_random'

    def lookups(self, request, model_admin):
        return (
            ('True', 'True'),
            ('False', 'False'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            new_queryset = []
            for query in queryset.all():
                if query.id[:11] == "IG-RAN-0000":
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == 'False':
            new_queryset = []
            for query in queryset.all():
                if query.id[:11] != "IG-RAN-0000":
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset


class OrderAdmin(ImportExportActionModelAdmin):
    resource_class = OrderResource
    list_display = ['id', "amount", "user", 'pay_for', 'transacted', 'transaction_status', 'is_random']
    list_filter = ['pay_for', OrderTransactedFilter, OrderTransactionStatusFilter, OrderIsRandomFilter]
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
