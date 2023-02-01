from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.conf import settings
from django.utils.html import mark_safe
from django.db.models.signals import pre_save, post_save

from allmarket.utils import unique_slug_generator



class ProductCategory(models.Model):
    title           = models.CharField(max_length=120, unique=True, db_index=True)
    color           = models.CharField(max_length=7, default='#007bff')
    updated_time    = models.DateTimeField(auto_now=True)
    created_time    = models.DateTimeField(auto_now_add=True)   

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.pk) + ' - ' + self.title

    def get_category_badge(self):
        title = escape(self.title)
        color = escape(self.color)
        html  = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, title)
        return mark_safe(html)


class SubCategory(models.Model):
    category        = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    title           = models.CharField(max_length=120, unique=True)   

    class Meta:
        verbose_name = 'Sub category'
        verbose_name_plural = 'Sub categories'

    def __str__(self):
        return self.title + ' - ' + (self.category.title)


class ColorVariation(models.Model):
    title = models.CharField(max_length=50)
    code  = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.title


class SizeVariation(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def sponsored(self):
        return self.filter(sponsored=True, active=True)

    def search(self, query):
        lookups = (
                  Q(title__icontains=query) | 
                  Q(description__icontains=query) |
                  Q(base_price__icontains=query) |
                  Q(origin__icontains=query) |
                  Q(manufacturer__icontains=query) |
                  Q(category__title__icontains=query) |
                  Q(sub_category__title__icontains=query) 
                  )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Product.objects.featured() 
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


def product_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Product_Images/seller/<filename>
    return 'Products_Images/{0}_{1}'.format(instance.pk, filename)

class Product(models.Model):

    NEW = 'New'
    USED = 'Used'
    REFURBISHED = 'Refurbished'    
    PRODUCT_CONDITION = (
        (NEW, 'New'),
        (USED, 'Used'),
        (REFURBISHED, 'Refurbished'),
    )

    img1            = models.ImageField(upload_to=product_image_path)
    img2            = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    img3            = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    img4            = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    img5            = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    video_link      = models.URLField(max_length=500, null=True, blank=True, help_text='http://')
    slug            = models.SlugField(blank=True, unique=True)   
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True)
    manufacturer    = models.CharField(max_length=120, null=True, blank=True, help_text='Make/Brand/Manufacturer')
    origin          = models.CharField(max_length=120, null=True, blank=True)
    condition       = models.CharField(max_length=120, choices=PRODUCT_CONDITION)    
    product_type    = models.CharField(max_length=120, null=True, blank=True, help_text='eg. Laptop, Engine, Building, Shirt, etc.')       
    category        = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='product_category')
    sub_category    = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, blank=True, null=True)

    color           = models.ManyToManyField(ColorVariation, blank=True)
    size            = models.ManyToManyField(SizeVariation, blank=True, help_text='')
    weight          = models.FloatField(null=True, blank=True, help_text='Value should be in kg')

    base_price      = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)   
    discount        = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)    
    shipping_in_city     = models.DecimalField(decimal_places=2, max_digits=15, default=0.00, null=True, blank=True)   
    shipping_in_country  = models.DecimalField(decimal_places=2, max_digits=15, default=0.00, null=True, blank=True)
    shipping_out_country = models.DecimalField(decimal_places=2, max_digits=15, default=0.00, null=True, blank=True)
    stock_initial   = models.PositiveIntegerField(default=1)  
    stock_remaining = models.PositiveIntegerField(default=0)    
    featured        = models.BooleanField(default=False)
    sponsored       = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    is_digital      = models.BooleanField(default=False) # User Library
    product_info    = models.TextField(null=True, blank=True)
    warranty_info   = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    shipping_info   = models.TextField(null=True, blank=True)

    #seller          = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='product_seller')    
    #batch           = ChainedForeignKey(
    #                                    ProductBatch, 
     #                                   chained_field='seller',
      #                                  chained_model_field='seller',
       #                                 show_all=True,
        #                                auto_choose=True,
         #                               sort=True, 
          #                              on_delete=models.CASCADE, related_name='product_batch')  
    #batch           = models.ForeignKey(ProductBatch, on_delete=models.CASCADE, related_name='product_batch')    

    updated_time    = models.DateTimeField(auto_now=True)
    created_time    = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def __str__(self):
        return f'{self.pk} - {self.title} ({self.slug}) - {self.stock_initial}'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:productDetails', kwargs={'slug': self.slug})
        #return reverse('products:productDetails', kwargs={'pk': self.pk})

    def get_add_to_cart_url(self):
        return reverse('orders:addToCart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('orders:removeFromCart', kwargs={'slug': self.slug})

    @property
    def get_name(self):
        return self.title

    #def get_downloads(self):
    #    qs = self.productfile_set.all()
    #    return qs

    def get_price (self):
        return self.base_price

    def get_discount (self):
        return self.discount
        
    def get_discounted_price(self):
        return self.get_price() - self.get_discount()

    def in_stock(self):
        if self.stock_initial > 0:
            return str(self.stock_initial)
        else:
            return None

    def get_category (self):
        return self.category.title

    def get_sub_category (self):
        return self.sub_category.title

    def title_and_description (self):
        return self.title +',' + ' ' + self.description

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product) 





#------------------------------------------------------------------------ tag

class Tag(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField(Product, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)



RATING_CHOICES = (
    ('FIVESTAR', '5 Stars'),
    ('FOURSTAR', '4 Stars'),
    ('THREESTAR', '3 Stars'),
    ('TWOSTAR', '2 Stars'),
    ('ONESTAR', '1 Star'),
)

class Review(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    product        = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    review_subject = models.CharField(max_length=100)
    review_rating  = models.CharField(max_length=9, choices=RATING_CHOICES)
    review_comment = models.TextField()
    updated_time   = models.DateTimeField(auto_now=True)
    created_time   = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.review_rating

    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-pk']


class DisplayImage(models.Model):
    slider1     = models.ImageField(upload_to='Display_images', blank=True, null=True, help_text='Dimension: 920 * 690')
    slider1a    = models.ImageField(upload_to='Display_images', blank=True, null=True, help_text='Dimension: 210 * 130')
    slider2     = models.ImageField(upload_to='Display_images', blank=True, null=True)
    slider2a    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    slider3     = models.ImageField(upload_to='Display_images', blank=True, null=True)
    slider3a    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    advertise1  = models.ImageField(upload_to='Display_images', blank=True, null=True)
    advertise2  = models.ImageField(upload_to='Display_images', blank=True, null=True)
    advertise3  = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display1    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display2    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display3    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display4    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display5    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display5    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display6    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display7    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display8    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display9    = models.ImageField(upload_to='Display_images', blank=True, null=True)
    display0    = models.ImageField(upload_to='Display_images', blank=True, null=True)

    def __str__(self):
        return str(self.pk)