from django.contrib import admin

from .models import Address, UserProfile
from .models import MarketingPreference




admin.site.site_header  = "Admin Login"
admin.site.site_title   = "Admin Portal"
admin.site.index_title  = "Welcome to Any Market"

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']

admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)


class MarketingPreferenceAdmin(admin.ModelAdmin):
    list_display  = ['__str__', 'subscribed', 'updated']
    readonly_fields = ['mailchimp_msg', 'mailchimp_subscribed', 'timestamp', 'updated']
    class Meta:
        model = MarketingPreference
        fields = [
                    'user', 
                    'subscribed', 
                    'mailchimp_msg',
                    'mailchimp_subscribed', 
                    'timestamp', 
                    'updated'
                ]

admin.site.register(MarketingPreference, MarketingPreferenceAdmin)