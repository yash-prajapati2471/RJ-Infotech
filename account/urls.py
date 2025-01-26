from django.urls import path
from .views import *

urlpatterns = [
    path('registration/',registration,name='registration'),
    path('login/',login,name='login'),

    path('verification/<uid64>/<token>',verification,name='verification'),

    path('logout/',logout,name='logout'),

    path('UserDashboard/',UserDashboard,name='UserDashboard'),
    path('forget_password/',forget_password,name='forget_password'),
    path('newpassword/',newpassword,name='newpassword'),
    path('password_reset_email/<uid64>/<token>/',password_reset_email,name='password_reset_email'),
    path('UserOrders/',UserOrders,name='UserOrders'),
    path('UserOrderDetails/<ordeid>/',UserOrderDetails,name='UserOrderDetails'),
    path('change_password/',change_password,name='change_password'),

    path('generate-invoice/<order_id>/',generate_invoice,name='generate_invoice'),
]
