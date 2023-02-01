from django.contrib import admin
from django.utils.html import mark_safe

from .models import Seller


# Register your models here.
'''
@admin.register(Seller)
class sellerAdmin(admin.ModelAdmin):

    readonly_fields     = ['owner', 'seller_Code']

    # seller model fields bahaviour
    empty_value_display = '--Empty--'
    exclude             = ('', ) # Fields that should not display
    list_display        = ('id', 'seller_Code', 'title', 'reg_Number', 'nature')
    list_filter         = ('nature',) 
    ordering            = ('-seller_Code',)
    search_fields       = ('title', 'seller_Code', 'reg_Number',)
    list_display_links  = ('id', 'seller_Code')

    # seller model fields grouping
    fieldsets = (

        ("Seller Logo:", {
            'fields': ('logo',)
        }),

        ("Seller Information:", {
            'fields': ('owner', 'seller_Code', 'title', 'reg_Number', 'nature', 'category')
        }),

        ("Seller Address:", {
            'fields': ('postal_Address', 'physical_Address', 'geo_Address', 'city', 
                'country', 'phone1', 'phone2', 'email', 'web')
        }),      
    )

    
    def logo_display(self, obj):
        return mark_safe(
            '<a href={url} target="_blank"><img src="{url}" width="{width}" \
            height={height} style={style} /></a>'.format(
                url     = obj.logo.url,
                width   = 200,
                height  = 200,
                style   = '',
            )
        )

    logo_display.short_description = "Seller Logo"
'''
'''
    def get_readonly_fields(self, request, obj=None):
        """ Make admission_no and date_of_admission uneditable if
        opened the admin change form but editable if opened
        the create form
        """

        if obj:  # if the object exists then make them readonly
            return ['reg_Number', 'title']
        else:
            return ['logo_display', ]
'''