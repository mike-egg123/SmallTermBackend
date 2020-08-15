from django.urls import path
from . import views

urlpatterns = [
    path('myjointeam', views.myjointeam),  # 加入的团队
    path('myjointeamYi', views.myjointeamYi),  # 加入的团队（异步）
    path('mycreateteam', views.mycreateteam),  # 创建的团队
    path('mycreateteamYi', views.mycreateteamYi),  # 创建的团队（异步）
    path('createteam', views.createteam),  # 创建团队
    path('jointeam', views.jointeam),  # 加入团队主页
    path('exitteam', views.exitteam),  # 退出团队
    path('disband', views.disband),  # 解散团队
    path('outteam', views.outteam),  # 踢人
    path('getteammember', views.getteammember), #查询团队成员
    path('getallarticles', views.getallarticles), # 查询团队文档,
    path('getteaminfo', views.getteaminfo) #查询团队信息

]
