from django.db import models
from django.contrib.auth.models import User

from article.models import *
from userprofile.models import *
# Create your models here.


#团队模型类

class Team(models.Model):
    tid = models.AutoField(primary_key=True) #主键
    tname = models.CharField(max_length=50) #团队名字
    tcreateuser = models.ForeignKey(User, on_delete=models.CASCADE) #创建者
    tmem = models.ManyToManyField(User, related_name='user') #团队成员（包括创建着）查询时用related_name 否则可能与创建者冲突
    tnum = models.PositiveIntegerField() #团队成员数
    tcreatetime = models.DateTimeField(auto_now_add=True) #团队创建时间

    def __str__(self):
        return 'Team {}'.format(self.tname)

#权限模型类
class Permissions(models.Model):
    pid = models.AutoField(primary_key=True) #主键
    state = models.IntegerField(blank=True) #权限值 0为私有 1为团队可见 2为团队可见可改
    uid = models.ForeignKey(User, on_delete=models.CASCADE) #用户外键
    did = models.ForeignKey(ArticlePost, on_delete=models.CASCADE) #文档外键
    tid = models.IntegerField(blank=True) #团队主键
    #团队外键没有设置外键，在私有时该值为-1，不对应任何团队

    def __str__(self):
        return 'Permission {}--{}'.format(self.uid.username, self.did.title)

#临时权限模型类
class Prepermission(models.Model):
    state = models.IntegerField(blank=True) #权限值 0为私有 1为团队可见 2为团队可见可改
    did = models.ForeignKey(ArticlePost, on_delete=models.CASCADE) #文档外键
    tid = models.IntegerField(blank=True) #团队主键

    def __str__(self):
        return '临时权限 {}--{}'.format(self.tid, self.did.title)



