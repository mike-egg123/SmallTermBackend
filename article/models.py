from django.db import models
# 导入内建的User
from django.contrib.auth.models import User
# 用于处理时间相关事务
from django.urls import reverse
from django.utils import timezone

# Create your models here.

# 文章栏目
class ArticleColumn(models.Model):
    title = models.CharField(max_length = 100, blank = True)
    created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title

class ArticlePost(models.Model):
    # 文章作者，外键为内建用户，on_delete = models.CASCADE表示如果用户注销了自己的账户，那么用这个账户发表过的所有文章也都删除
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    # 文章标题，CharField用于存较短的字符串，如标题
    title = models.CharField(max_length = 100)
    # 文章正文，TextFiled用于保存大量文本
    body = models.TextField()
    # 创建时间，参数表示在创建数据时默认写入当前时间
    created = models.DateTimeField(default = timezone.now)
    # 最后一次修改者
    last_updater = models.CharField(max_length = 10, blank = True)
    # 更新时间，参数表示每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now = True)
    # 是否在回收站
    is_in_garbage = models.BooleanField(default = False)


    class Meta:
        # ordering指定返回数据的排列顺序
        # -created表示按照创建时间倒序
        ordering = ('-created',)

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args = [self.id])

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete = models.CASCADE)
    liked = models.ForeignKey(ArticlePost, on_delete = models.CASCADE)
    def __str__(self):
        return self.liker.username + " likes " + self.liked.title


