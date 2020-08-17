from django.urls import path
from . import views

urlpatterns = [
    path('sendmessage', views.sendmessage),  # 发送私信
    path('getmessage', views.getmessage),  # 接收私信
    path('deletemessage', views.deletemessage)  # 删除私信

]