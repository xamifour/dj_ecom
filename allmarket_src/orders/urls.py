from django.urls import path

from .views import ( 
	CheckoutView, AddCouponView, remove_from_cart, OrderSummaryView, RefundRequestCreateView, 
	add_to_cart, reduce_single_item_in_cart, PaymentView, checkout_complete_view,
    OrderListView, OrderDetailsView, RefundRequestListView, OrderReceivedView, order_update_view 
	)



app_name = 'orders'

urlpatterns = [
    path('order-summary/', OrderSummaryView.as_view(), name='orderSummary'),
    path('add-to-cart/<slug>/', add_to_cart, name='addToCart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='removeFromCart'),
    path('reduce-single-item/<slug>/', reduce_single_item_in_cart, name='reduceSingleItemInCart'),  
    path('checkout/', CheckoutView.as_view(), name='checkout'),   
    path('add-coupon/', AddCouponView.as_view(), name='addCoupon'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('checkout-complete/', checkout_complete_view, name='checkoutComplete'),

    path('orderList/', OrderListView.as_view(), name='orderList'),
    path('order/<int:pk>/', OrderDetailsView.as_view(), name='orderDetails'),
    path('refunds/', RefundRequestListView.as_view(), name='refundRequestList'),
    path('requestRefund/', RefundRequestCreateView.as_view(), name='refundRequestCreate'),
    path('order-received/', OrderReceivedView.as_view(), name='orderReceivedCreate'),
    path('order-update/<int:pk>/', order_update_view, name='orderUpdate'),
    #path('order-details/<int:pk>/', order_details_view, name='orderDetails'),
]