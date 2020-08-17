from django.db import models
from django.contrib.auth.models import User
from userprofile.models import *

# Create your models here.
class Message(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE) #消息发送用户
    message = models.CharField(max_length=300) #消息内容
    time = models.DateTimeField(auto_now_add=True) #时间
    tuid = models.ForeignKey(User, related_name='Tuser', on_delete=models.CASCADE) #消息接收人

    def __str__(self):
        return 'Message {}'.format(self.message)