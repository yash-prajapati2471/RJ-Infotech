from django.contrib import admin
from .models import registration,UserProfile
# Register your models here.

admin.site.register(registration)
admin.site.register(UserProfile)