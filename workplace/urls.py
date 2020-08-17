from django.urls import path
from . import views

urlpatterns = [
    path('myjointeam', views.myjointeam),  # 加入的团队
    path('myjointeamYi', views.myjointeamYi),  # 加入的团队（异步）
    path('mycreateteam', views.mycreateteam),  # 创建的团队
    path('mycreateteamYi', views.mycreateteamYi),  # 创建的团队（异步）
    path('myallteam', views.myallteam),  # 查询所拥有的所有团队
    path('createteam', views.createteam),  # 创建团队
    path('jointeam', views.jointeam),  # 加入团队主页
    path('exitteam', views.exitteam),  # 退出团队
    path('disband', views.disband),  # 解散团队
    path('outteam', views.outteam),  # 踢人
    path('getteammember', views.getteammember), #查询团队成员
    path('getallarticles', views.getallarticles), # 查询团队文档,
    path('getteaminfo', views.getteaminfo), #查询团队信息
    path('setpermission', views.setpermission),  # 设置（修改）文档权限
    path('getteamdoc', views.getteamdoc),  # 查询团队文档
    path('searchdoc', views.searchdoc),  # 查找文档（全局搜索的文档部分）
    path('searchteam', views.searchteam),  # 查找文档（全局搜索的文档部分）
    path('getpermission', views.getpermission), # 查询权限
    path('getpermissionsetting', views.getpermissionsetting),  # 查询权限设置
]
