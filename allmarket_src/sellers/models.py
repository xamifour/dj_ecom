from django.db import models
from django.urls import reverse

#from accounts.models import User



# Create your models here.

def seller_logo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.seller_Code, filename)
    # file will be uploaded to MEDIA_ROOT/Seller_Logo/seller_Code/<filename>    
    return 'Seller_Logo/{0}_{1}'.format(instance.seller_Code, filename)

class Seller(models.Model):

    GOODS    = 'Goods'
    SERVICES = 'Services'
    BOTH     = 'Both'    
    seller_NATURE = (
        (GOODS, 'Goods'),
        (SERVICES, 'Services'),
        (BOTH, 'Both'),
    )

    PROFESSIONAL    = 'Professional seller'
    ON_THE_GO = 'On the go seller'  
    SELLER_TYPE = (
        (PROFESSIONAL, 'Professional seller'),
        (ON_THE_GO, 'On the go seller'),
    )

    #owner           = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='seller')
    seller_Code     = models.CharField(max_length=20, unique=True) 	
    slug            = models.SlugField(blank=True, unique=True)
    seller_Type     = models.CharField(max_length=20, choices=SELLER_TYPE)     
    title           = models.CharField(max_length=120,  unique=True)
    logo            = models.ImageField(upload_to=seller_logo_path, null=True, blank=True)    
    reg_Number      = models.CharField(max_length=120,  null=True, blank=True)
    nature          = models.CharField(max_length=20, choices=seller_NATURE)  
    category        = models.ForeignKey(to='products.ProductCategory', on_delete=models.CASCADE, null=True, blank=True, related_name='seller_category')           
    postal_Address  = models.CharField(max_length=120,  null=True, blank=True)
    physical_Address= models.CharField(max_length=120,  null=True, blank=True)
    geo_Address     = models.CharField(max_length=120,  null=True, blank=True)
    city            = models.CharField(max_length=120,  null=True, blank=True)
    country         = models.CharField(max_length=120,  null=True, blank=True)
    phone1          = models.CharField(max_length=120,  null=True, blank=True)    
    phone2          = models.CharField(max_length=120,  null=True, blank=True)
    email           = models.EmailField(max_length=120,  null=True, blank=True)    
    web             = models.URLField('Web Address', max_length=120,  null=True, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)


    @property
    def detail(self):
        return '{} Class - {}'.format(self.seller_Code, self.title)
        
    def __str__(self):
        return self.seller_Code    

    #Reverse to sellers app, sellers detail page using self.pk
    def get_absolute_url(self):
        return reverse('sellers:seller_details', kwargs={'pk': self.pk})    


class ProductBatch(models.Model):
    seller          = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='batch_seller')
    title           = models.CharField(max_length=120)         
    arrival_Date    = models.DateField(verbose_name=None, null=True, blank=True)
    origin          = models.CharField(max_length=120, null=True, blank=True)
    destination     = models.CharField(max_length=120, null=True, blank=True)  
    description     = models.TextField(null=True, blank=True)       
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} {self.title} ({self.seller})'

    class meta:
        ordering = ['-pk']
        
    # Reverse to products app, product_seller_details page using self.pk
    def get_absolute_url(self):
        return reverse('products:product_seller_details', kwargs={'pk': self.pk})    

