from django.contrib import admin
# 导入ArticlePost模块
from .models import ArticlePost, ArticleColumn

# Register your models here.
# 注册到admin中
admin.site.register(ArticlePost)
admin.site.register(ArticleColumn)
