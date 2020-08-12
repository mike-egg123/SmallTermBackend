from django import template
from django.utils import timezone
import math

register = template.Library()
# 若注册装饰器中携带了name参数，则其值为此filter的名称；若未携带，则函数名就是filter的名称。
@register.filter(name = 'transfer')
def transfer(value, arg):
    return arg

@register.filter()
def lower(value):
    return value.lower()

# 获取相对时间
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value
    # 一分钟之内
    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'
    # 一小时之内
    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"
    # 一天之内
    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"
    # 一个月之内
    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"
    # 一年之内
    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"
    # 几年前
    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"

@register.inclusion_tag('article/tag_list.html')
def show_comments_pub_time(article):
    """显示文章评论的发布时间"""
    comments = article.comments.all()
    return {'comments': comments}