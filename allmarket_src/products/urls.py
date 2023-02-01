from django.urls import path
from .views import ( 
	ProductSearchView,
	#ProductDetailView,
	productDetailView, 
	ProductComparisonView,
	reviewCreateView
	)



app_name = 'products'

urlpatterns = [
	path('qs', ProductSearchView.as_view(), name='productQuery'),
	#path('product/<slug>/', ProductDetailView.as_view(), name='productDetails'),
	path('product/<slug>/', productDetailView, name='productDetails'),
	path('product-comparison/', ProductComparisonView.as_view(), name='productComparison'),	
	path('product/<slug>/create-review/', reviewCreateView, name='productReviewCreate'),	
]
