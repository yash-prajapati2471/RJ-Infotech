from django.urls import path
from orders.views import *

urlpatterns = [
    path('place_order/',place_order,name='orderproduct'),
    path('payment/',payment,name='payment'),
]
