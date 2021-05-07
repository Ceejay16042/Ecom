from django.conf.urls import url
from django.urls import path
from my_app import views

# app_name = 'basic_app'

urlpatterns = [
    url('checkout', views.checkout, name="checkout"),
    path('store', views.store, name="store"),
    path('cart', views.cart, name="cart"),
    path('update_item/', views.updateitem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order")
]
