from django.urls import path
from .views import *

urlpatterns = [
    path('registration/',registration,name='registration'),
    path('login/',login,name='login'),

    path('verification/<uid64>/<token>',verification,name='verification'),

    path('logout/',logout,name='logout'),
]
