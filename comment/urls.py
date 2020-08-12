# 引入path
from django.urls import path
from . import views
# 正在部署的应用名称
app_name = 'comment'
# url列表
urlpatterns = [
    # 处理一级回复
    path('post-comment/<int:article_id>/', views.post_comment, name = 'post_comment'),
    # 处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
]