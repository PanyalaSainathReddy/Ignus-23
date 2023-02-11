from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import (AlumniConfirmPresence, AlumniContribution, BulkOrder,
                     BulkTransaction, Order, PromoCode, Transaction)


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
                if query.transacted():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == 'False':
            new_queryset = []
            for query in queryset.all():
                if not query.transacted():
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
                if query.transaction_status() == self.value():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == "TXN_FAILURE":
            new_queryset = []
            for query in queryset.all():
                if query.transaction_status() == self.value():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == "PENDING":
            new_queryset = []
            for query in queryset.all():
                if query.transaction_status() == self.value():
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
                if query.is_random():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == 'False':
            new_queryset = []
            for query in queryset.all():
                if not query.is_random():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset


class OrderAdmin(ImportExportActionModelAdmin):
    resource_class = OrderResource
    list_display = ['id', "amount", "user", 'pay_for', 'promo_code', 'transacted', 'transaction_status', 'is_random']
    list_filter = ['pay_for', 'promo_code__code', OrderTransactedFilter, OrderTransactionStatusFilter, OrderIsRandomFilter]
    search_fields = ['id', 'user__user__first_name', 'user__user__last_name', 'user__registration_code']


class BulkOrderAdmin(admin.ModelAdmin):
    list_display = ['id', "amount", 'pay_for', 'transacted', 'transaction_status']
    list_filter = ['pay_for', OrderTransactedFilter, OrderTransactionStatusFilter]
    search_fields = ['id']


class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('txn_id', 'bank_txn_id', 'status', 'order__id', 'amount', 'gateway_name', 'payment_mode', 'resp_code', 'resp_msg', 'timestamp', 'user__registration_code', 'user__user__first_name', 'user__user__last_name')


class TransactionAdmin(ImportExportActionModelAdmin):
    resource_class = TransactionResource
    list_display = ['txn_id', "order", "amount", "user", "status"]
    list_filter = ['status', 'order__promo_code__code']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__registration_code', 'status', 'order__id', 'txn_id']


class BulkTransactionAdmin(admin.ModelAdmin):
    list_display = ['txn_id', "order", "amount", "status"]
    list_filter = ['status']
    search_fields = ['status', 'order__id', 'txn_id']


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'uses', 'max_uses', 'pass_name', 'discounted_amount', 'valid']
    list_filter = ['valid']
    search_fields = ['code', 'pass_name', 'discounted_amount']


class AlumniConfirmPresenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'passing_year']
    search_fields = ['name', 'email']

    class Meta:
        model = AlumniConfirmPresence


class AlumniContributionTransactedFilter(admin.SimpleListFilter):
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
                if query.transacted():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == 'False':
            new_queryset = []
            for query in queryset.all():
                if not query.transacted():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset


class AlumniContributionTransactionStatusFilter(admin.SimpleListFilter):
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
                if query.transaction_status() == self.value():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == "TXN_FAILURE":
            new_queryset = []
            for query in queryset.all():
                if query.transaction_status() == self.value():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset
        if self.value() == "PENDING":
            new_queryset = []
            for query in queryset.all():
                if query.transaction_status() == self.value():
                    new_queryset.append(query.id)
            new_queryset = queryset.filter(id__in=new_queryset)
            return new_queryset


class AlumniContributionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'passing_year', 'amount', 'order', 'transacted', 'transaction_status']
    search_fields = ['name', 'email']
    list_filter = ['passing_year', AlumniContributionTransactedFilter, AlumniContributionTransactionStatusFilter]

    class Meta:
        model = AlumniContribution


admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BulkOrder, BulkOrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(BulkTransaction, BulkTransactionAdmin)
admin.site.register(AlumniConfirmPresence, AlumniConfirmPresenceAdmin)
admin.site.register(AlumniContribution, AlumniContributionAdmin)
