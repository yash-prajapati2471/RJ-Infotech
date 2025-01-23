from django.urls import path
from orders.views import *

urlpatterns = [
    path('payment',orderproduct,name='orderproduct')
]
