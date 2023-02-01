from django.contrib import admin

from .models import OrderProduct, Order, Payment, Coupon, Refund, OrderReceived


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):

    # seller model fields grouping
    fieldsets = (

        ("USER:", {
            'fields': ('user', 'shipping_address', 'billing_address')
        }),

        ("ORDER:", {
            'fields': ('get_order_id', 'ordered_date', 'order_subtotal', 'order_total', 
            'coupon', 'payment', 'items',)
        }),

        ("STATUS:", {
            'fields': ('status', 'ordered', 
            ('being_delivered', 'being_received', 'refund_requested', 'refund_granted'))
        }),      
    )    

    readonly_fields = [
                    'get_order_id', 'user', 'ordered_date', 'shipping_address', 'billing_address', 
                    'payment', 'order_subtotal', 'order_total', 'coupon', 'items'
                    ]
    list_display =  [
                    'user',
                    'get_order_id',
                    'order_total',
                    'ordered_date',
                    'ordered',
                    'payment',
                    #'being_delivered',
                    #'being_received',
                    #'refund_requested',
                    #'refund_granted',
                    #'shipping_address',
                    'billing_address',
                    #'coupon'
                    ]
    list_display_links = [
                    'user',
                    'get_order_id',
                    #'shipping_address',
                    'billing_address',
                    'payment',
                    #'coupon'
                    ]
    list_filter =   [
                    'ordered',
                    'being_delivered',
                    'being_received',
                    'refund_requested',
                    'refund_granted'
                    ]
    search_fields = [
                    'user__username',
                    'ref_code'
                    ]
    actions = [make_refund_accepted]



admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(OrderReceived)