from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Team) #注册team表
admin.site.register(Permissions) #注册Permission表
admin.site.register(Prepermission) #注册Prepermission表