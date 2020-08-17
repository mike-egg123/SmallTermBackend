from django.db import models
from django.contrib.auth.models import User

from workplace.models import *
from article.models import *
from userprofile.models import *

class Teammessage(models.Model):
    messagetype = models.IntegerField() #消息类型码
    tid = models.ForeignKey(Team, on_delete=models.CASCADE) #团队
    uid = models.ForeignKey(User, on_delete=models.CASCADE) #消息发起人
    message = models.CharField(max_length=500) #消息内容
    time = models.DateTimeField(auto_now_add=True) #时间
    tuid = models.ForeignKey(User, related_name='Touser', on_delete=models.CASCADE) #消息接收人

    def __str__(self):
        return 'message {}'.format(self.message)

class Commentmessage(models.Model):
    messagetype = models.IntegerField(default=9)  # 消息类型码
    aid = models.ForeignKey(ArticlePost, on_delete=models.CASCADE) #评论文档
    uid = models.ForeignKey(User, on_delete=models.CASCADE) #评论用户
    time = models.DateTimeField(auto_now_add=True)  #时间
    tuid = models.ForeignKey(User, related_name='Couser', on_delete=models.CASCADE) #消息接收人
    message = models.CharField(max_length=500)  # 消息内容

    def __str__(self):
        return 'message {}'.format(self.message)
