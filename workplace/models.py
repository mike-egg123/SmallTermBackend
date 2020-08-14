from django.db import models
from django.contrib.auth.models import User

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



