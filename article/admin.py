from django.contrib import admin
# 导入ArticlePost模块
from .models import *

# Register your models here.
# 注册到admin中
admin.site.register(ArticlePost)
admin.site.register(Like)
admin.site.register(WatchingRecord)

