from django.contrib import admin
from django.utils.html import mark_safe

from .models import (
	Product, 
	ProductCategory,
	SubCategory,
	ColorVariation,
	SizeVariation,
	Review,
    DisplayImage,
)



#----------------------------------------------------------------------- Product
#Display Class of Product Model in Admin Panel

class ProductAdmin(admin.ModelAdmin):
    empty_value_display = '--Empty--'
    exclude             = ('', ) # Fields that should not display
    list_display        = ('id', 'title', 'manufacturer', 'condition', 'origin', 'sub_category', 'base_price')
    list_filter         = ('condition', 'origin', 'category') 
    ordering            = ('-pk',)
    search_fields       = ('title', 'manufacturer', 'condition', 'product_type')
    list_display_links  = ('id', 'title')
    #list_select_related = ('seller', 'batch')
    readonly_fields     = ['slug',]
    #disabled_fields = ['base_price',]
    list_editable 		= ['base_price']
    
    # Display style image
    def profile_image_display(self, obj):
        return mark_safe(
            '<a href={url} target="_blank"><img src="{url}" width="{width}" \
            height={height} style={style} /></a>'.format(
                url=obj.img.url,
                width=200,
                height=200,
                style='',
            )
        )
    profile_image_display.short_description = "Product Image"



admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(SubCategory)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)
admin.site.register(Review)
admin.site.register(DisplayImage)
