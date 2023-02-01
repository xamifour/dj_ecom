"""
allmarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from products.views import homeView



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', TemplateView.as_view(template_name="index.html")),
    #path('', HomeView.as_view(), name='home'),
    path('', homeView, name='home'),
    path('accounts/', include('allauth.urls')),

    path('orders/', include('orders.urls', namespace='orders')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('products/', include('products.urls', namespace='products')),
    #path('sellers/', include('sellers.urls', namespace='sellers')),
    path('api/', include('allapi.urls', namespace='allapi')),  # add this line

    path('contactus/', TemplateView.as_view(template_name='contact.html'), name='contactus'),    
]



if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
