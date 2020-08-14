from django.urls import path
from . import views

urlpatterns = [
    path('myteam', views.myteam),  # 加入的团队
    path('createteam', views.createteam),  # 创建团队
    path('jointeam', views.jointeam),  # 加入团队主页
    path('exitteam', views.exitteam),  # 退出团队
    path('disband', views.disband),  # 解散团队
    path('outteam', views.outteam),  # 踢人
    path('getteammember', views.getteammember), #查询团队成员
    path('getallarticles', views.getallarticles)  # 查询团队文档

]
