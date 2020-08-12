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
    path('apis/user/getstatus', Users.get_status),  # 返回状态 是否登录
    path('apis/user/login', Users.login_user),  # 登录
    path('apis/user/logout', Users.logout_user),  # 注销
    path('apis/user/register', Users.register),  # 注册
    path('apis/personality/change', Personality.change_personality), #修改用户信息
    path('apis/personality/get', Personality.get_personality), # 得到用户信息
    path('apis/article/create', Article.article_create), # 文档的创建
    path('apis/article/update', Article.article_update),  # 文档的修改
    path('apis/article/get', Article.article_get),  # 文档的修改
    path('apis/article/delete', Article.article_remove),  # 文档的修改

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
