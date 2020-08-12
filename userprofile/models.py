from django.db import models
from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    # 与User模型形成一对一的映射关系
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')
    # 电话号码字段
    phone = models.CharField(max_length = 20, blank = True)
    # 头像
    avatar = models.ImageField(upload_to = "avatar/%Y%m%d/", blank = True)
    # 个人简介
    bio = models.TextField(max_length = 500, blank = True)
    # 用户id
    userid = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

# 会导致bug出现：在后台中创建User时如果填写了Profile任何内容，则系统报错且保存不成功；其他情况下均正常
# # 信号接收函数，每当新建User实例时自动调用
# @receiver(post_save, sender = User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user = instance)
#
# # 信号接收函数，每当更新User实例时自动调用
# @receiver(post_save, sender = User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
