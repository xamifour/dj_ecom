from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django_countries.fields import CountryField

from allmarket.utils import Mailchimp


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_fullname(self):
        return self.user.first_name + ' ' + self.user.last_name


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Address(models.Model):
    user              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address    = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country           = CountryField(multiple=False)
    zip               = models.CharField(max_length=100)
    address_type      = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default           = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.street_address})"

    class Meta:
        verbose_name_plural = 'Addresses'




#------------------------------------------------------------------------ marketing

class MarketingPreference(models.Model):
    user                    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed              = models.BooleanField(default=True)
    mailchimp_subscribed    = models.BooleanField(null=True, blank=True)
    mailchimp_msg           = models.TextField(null=True, blank=True)
    updated                 = models.DateTimeField(auto_now=True)
    timestamp               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = Mailchimp().subscribe(instance.user.email)
        print(status_code, response_data)


post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)

def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            # subscribing user
            status_code, response_data = Mailchimp().subscribe(instance.user.email)
        else:
            # unsubscribing user
            status_code, response_data = Mailchimp().unsubscribe(instance.user.email)

        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data

pre_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)


def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    
    #User model
    
    if created:
        MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)