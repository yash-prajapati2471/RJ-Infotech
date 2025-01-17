from django.urls import path
from carts.views import *

urlpatterns = [
    path('',cart,name='cart'),
    path('add_to_cart/<product_id>',add_to_cart,name='add_to_cart'),
    path('decrease/<product_id>/<cart_item_id>',decrease,name='decrease'),
    path('plus/<product_id>/<cart_item_id>',plus,name='plus'),

    path('cheakout',cheakout,name='cheakout'),
]
