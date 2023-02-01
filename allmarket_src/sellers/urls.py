from django.urls import path
from .views import *
 
app_name = 'sellers'

urlpatterns = [	

	#---------------------- seller    
    path('seller/add/', SellerCreateView.as_view(), name='seller_add'),
    path('', SellerListView.as_view(), name='seller_list'),
    path('seller/<int:seller_id>/details/', sellerDetailsView, name='seller_details'),
    path('seller/<int:pk>/update/', SellerUpdateView.as_view(), name='seller_update'),
    path('seller/<int:pk>/delete/', SellerDeleteView.as_view(), name='seller_delete'),   
    path('sellerstat', sellerStatView, name='seller_stat'),

	#---------------------- product batch
	path('seller/<int:pk>/productbatch/add/', productBatchAddView, name='productbatch_add'),
	path('seller/<int:seller_id>/productbatch/<int:productbatch_id>/details/', productBatchDetailsView, name='productbatch_details'),

    path('seller/<int:seller_id>/productbatch/<int:productbatch_id>/update/', productBatchUpdateView, name='productbatch_update'),
    path('seller/<int:seller_id>/productbatch/<int:productbatch_id>/delete/', ProductBatchDeleteView.as_view(), name='productbatch_delete'),

]