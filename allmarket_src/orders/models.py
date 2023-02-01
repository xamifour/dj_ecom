from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from decimal import Decimal
from django.db.models.signals import pre_save, post_save

from products.models import Product
from profiles.models import Address



ORDER_STATUS_CHOICES = (
    ('cancelled', 'cancelled'),
    ('created', 'Created'),
    ('shipped', 'Shipped'),
    ('received', 'Received'),
    ('refund_requested', 'Refunded Requested'),
    ('refund_granted', 'Refund Granted'),
)


class OrderProduct(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered  = models.BooleanField(default=False)
    item     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_item_qty_amount(self):
        return self.quantity * self.item.get_discounted_price()

    def get_item_total_discount(self):
        return self.quantity * self.item.get_discount()

    def get_amount_saved_on_item(self):
        return (self.item.get_price() - self.item.get_discounted_price()) * self.quantity

    def get_item_final_amount(self):
        return self.get_item_qty_amount()

    def get_product_qty_left(self):
        return self.item.stock_initial - self.quantity


class Order(models.Model):
    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code         = models.CharField(max_length=20, blank=True, null=True)
    items            = models.ManyToManyField(OrderProduct)
    start_date       = models.DateTimeField(auto_now_add=True)
    ordered_date     = models.DateTimeField()
    ordered          = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address  = models.ForeignKey(
        Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment          = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon           = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    order_subtotal   = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    order_total      = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    status           = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    being_delivered  = models.BooleanField(default=False)
    being_received   = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted   = models.BooleanField(default=False)
    updated_time     = models.DateTimeField(auto_now=True)
    created_time     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} - {self.user.username} ({self.ref_code}) ({self.order_total})"

    class Meta:
        ordering = ['-ordered_date']

    def get_absolute_url(self):
        return reverse('orders:orderDetails', kwargs={'pk': self.pk})

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_item_final_amount()
        if self.coupon:
            total -= self.coupon.amount
        self.order_subtotal = total
        self.save()
        return total

    def get_total_qty_buying(self):
        total_qty_purchased = 0
        for order_item in self.items.all():
            total_qty_purchased += order_item.quantity
        return total_qty_purchased

    def get_order_subtotal(self):
        return self.order_subtotal

    def get_order_total(self):
        return self.order_total

    def get_order_id(self):
        return self.ref_code

    def get_order_status(self):# needs a fix
        if self.being_delivered:
            return 'Delivered'
        elif self.being_received:
            return 'Received'
        elif self.refund_requested:
            return 'Refund Requested'
        elif self.refund_granted:
            return 'Refund Granted'
        else:
            return 'Ordered'

'''
    def get_order_status(self):
    # needs a fix, using status field instead of boolean
        if self.status == "shipped":
            return "Shipped"
        elif self.status == "received":
            return "Received"
        elif self.status == "refund_requested":
            return "Refunded Requested"
        elif self.status == "refund_granted":
            return "Refund Granted"
        elif self.status == "cancelled":
            return "Cancelled"
        return "Shipping Soon"
'''

def order_post_save_receiver(sender, instance, *args, **kwargs):
    sales_tax = 2 # 8% tax
    if instance.order_subtotal > 0:
        instance.order_total = Decimal(instance.order_subtotal) + Decimal(sales_tax)
    else:
        instance.order_total = 0.00

post_save.connect(order_post_save_receiver, sender=Order)


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.amount})"


class Coupon(models.Model):
    code   = models.CharField(max_length=15)
    amount = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} - {self.code} ({self.amount})"


class Refund(models.Model):
    order        = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason       = models.TextField()
    accepted     = models.BooleanField(default=False)
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} - {self.order.ref_code} ({self.order})"


class OrderReceived(models.Model):
    order        = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} - {self.order.ref_code}"