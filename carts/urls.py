from django.urls import path
from carts.views import *

urlpatterns = [
    path('',cart,name='cart'),
    path('add_to_cart/<product_id>',add_to_cart,name='add_to_cart'),
]
