from django.urls import path
from allapi import views


app_name = 'allapi'

urlpatterns = [
    path('', views.NoteList.as_view()),
    path('<int:pk>/', views.NoteDetail.as_view()),

    path('product-list/', views.ProductList.as_view()),
    path('product/<int:pk>/', views.ProductDetail.as_view()),
]