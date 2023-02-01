from django.urls import path

from .views import UserProfileView, WishlistView
from .views import MarketingPreferenceUpdateView, MailchimpWebhookView


app_name = 'profiles'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='userProfile'),
    path('wishlist/', WishlistView.as_view(), name='userWishlist'),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='emailMarketing'),
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooksMailchimp'),

]