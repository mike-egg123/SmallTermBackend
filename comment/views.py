import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from notifications.signals import notify
from django.contrib.auth.models import User
from django.http import JsonResponse

from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment
from django.core import serializers

# Create your views here.
# 这里别看！
# 文章评论
@login_required(login_url = '/userprofile/login/')
def post_comment(request, article_id, parent_comment_id = None):
    article = get_object_or_404(ArticlePost, id = article_id)

    # 处理post请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit = False)
            new_comment.article = article
            new_comment.user = request.user
            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id = parent_comment_id)
                # 若回复级超过二级，则转换成二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # 二级回复之间的消息通知，被回复人与发表回复的不是同一个人才会发出消息
                if request.user != parent_comment.user:
                    notify.send(
                        request.user,
                        recipient = parent_comment.user,
                        verb = '回复了你',
                        target = article,
                        action_object = new_comment,
                    )
                # 二级回复的消息发送给管理员
                notify.send(
                    request.user,
                    recipient = User.objects.filter(is_superuser = 1),
                    verb = '回复了{}'.format(parent_comment.user),
                    target = article,
                    action_object = new_comment,
                )
                # return HttpResponse('200 OK')
                return JsonResponse({"code":"200 OK", "new_comment_id":new_comment.id})
            new_comment.save()
            # 一级评论之间的消息通知，被评论人与发表评论的不是同一个人才会发出消息
            if request.user != article.author:
                notify.send(
                    request.user,
                    recipient = article.author,
                    verb = '评论了你',
                    target = article,
                    action_object = new_comment,
                )
            # 一级评论的消息发送给管理员
            notify.send(
                request.user,
                recipient=User.objects.filter(is_superuser=1),
                verb='评论了{}'.format(article.author),
                target=article,
                action_object=new_comment,
            )
            redirect_url = article.get_absolute_url() + "#comment_elem_" + str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse('表单内容有误，请重新填写！')
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form':comment_form,
            'article_id':article_id,
            'parent_comment_id':parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse('仅接受get/post请求')
# 这里开始！
class CommentViews:
    # 发表评论
    @staticmethod
    def post(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            articleid = data.get('articleid')
            userid = data.get('userid')
            content = data.get('content')
            comment = Comment.objects.create(article_id=articleid, user_id=userid, body=content)
            comment.save()
            return JsonResponse({
                "status":0,
                "message":"success"
            })
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })
    # 获取对应文章的所有评论
    @staticmethod
    def get_comments_by_articleid(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            articleid = data.get('articleid')
            comments = Comment.objects.filter(article_id=articleid)
            json_list = []
            for comment in comments:
                json_dict = {}
                json_dict["content"] = comment.body
                json_list.append(json_dict)
            return JsonResponse(json_list, safe=False)
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })
