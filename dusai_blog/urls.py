"""dusai_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import notifications.urls
from article.views import article_list
from userprofile.views import Users, Personality
from article.views import Article
from comment.views import CommentViews

urlpatterns = [
    # home
    path('', article_list, name = 'home'),
    # 后台管理
    path('admin/', admin.site.urls),
    # 文章管理
    path('article/', include('article.urls', namespace='article')),
    # 用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    # 用户密码重置
    path('password-reset/', include('password_reset.urls')),
    # 评论
    path('comment/', include('comment.urls', namespace = 'comment')),
    # 消息通知
    path('inbox/notifications/', include(notifications.urls, namespace = 'notifications')),
    # notice
    path('notice/', include('notice.urls', namespace = 'notice')),
    # 第三方登录
    path('accounts/', include('allauth.urls')),
    path('apis/workplace/', include('workplace.urls')),  # 个人工作平台
    path('apis/user/getstatus', Users.get_status),  # 返回状态 是否登录
    path('apis/user/login', Users.login_user),  # 登录
    path('apis/user/getvalidcode', Users.get_valid_img),  # 获取验证码
    path('apis/user/logout', Users.logout_user),  # 注销
    path('apis/user/register', Users.register),  # 注册
    path('apis/personality/change', Personality.change_personality), #修改用户信息
    path('apis/personality/get', Personality.get_personality), # 得到用户信息
    path('apis/article/create', Article.article_create), # 文档的创建
    path('apis/article/update', Article.article_update),  # 文档的修改
    path('apis/article/updateYi', Article.article_updateYi),  # 文档的修改（异步）
    path('apis/article/get', Article.article_get),  # 文档的查看
    path('apis/article/getreadonly', Article.article_get_readonly),  # 文档的查看（只读）
    path('apis/article/delete', Article.article_remove),  # 文档的删除
    path('apis/article/recover', Article.article_recover),  # 文档的恢复（从回收站）
    path('apis/article/likeornot', Article.article_like),  # 文档的收藏
    path('apis/article/updatingcodechange', Article.change_updating),  # 文档的修改状态的改变
    path('apis/article/getrecentwatch', Article.get_recent_watch),  # 获取最近浏览
    path('apis/article/getalllikes', Article.get_all_likes),  # 获取所有收藏
    path('apis/article/getallcreations', Article.get_all_creations),  # 获取所有创建的文档
    path('apis/article/getallcreationsingarbage', Article.get_all_creations_in_garbage),  # 获取回收站中的所有文档
    path('apis/article/getrecentwatchYi', Article.get_recent_watchYi),  # 获取最近浏览（异步）
    path('apis/article/getalllikesYi', Article.get_all_likesYi),  # 获取所有收藏（异步）
    path('apis/article/getallcreationsYi', Article.get_all_creationsYi),  # 获取所有创建的文档（异步）
    path('apis/article/getallcreationsingarbageYi', Article.get_all_creations_in_garbageYi),  # 获取回收站中的所有文档（异步）
    path('apis/article/addlock', Article.addlock),  # 给文档加锁
    path('apis/article/releaselock', Article.releaselock),  # 给文档解锁
    path('apis/comment/post', CommentViews.post),  # 发表评论
    path('apis/comment/getbyarticleid', CommentViews.get_comments_by_articleid),  # 获得对应文档的评论
    path('apis/search/users', Personality.searchuser),  # 全局搜索用户
    path('apis/message/', include("message.urls")), # 消息通知
    path('apis/chat/', include("chat.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
