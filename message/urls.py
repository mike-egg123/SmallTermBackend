from django.urls import path
from . import views

urlpatterns = [
    path('getuser', views.getuser),  # 查找邀请用户

    path('invite', views.invite),  # 邀请用户加入团队
    path('refuseinvitation', views.refuseinvitation),  #拒绝邀请
    path('agreeinvitation', views.agreeinvitation),  #同意邀请生成消息通知

    path('apply', views.apply),  # 申请加入团队
    path('agreeapply', views.agreeapply),  #同意申请生成消息通知
    path('refuseapply', views.refuseapply),  #拒绝申请

    path('outteammessage', views.outteammessage),  #踢人生成消息通知
    path('exitteammessage', views.exitteammessage),  #退出团队生成消息通知

    path('commentmessage', views.commentmessage),  # 评论生成消息通知

    path('solveteammessage', views.solveteammessage),  #团队消息通知处理(已读/忽略)
    path('solvecommentmessage', views.solvecommentmessage),  #评论消息通知处理

    path('getmessage', views.getmessage)  # 接收消息

]