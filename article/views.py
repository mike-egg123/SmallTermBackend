import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import ArticlePost, ArticleColumn
from .forms import ArticlePostForm
from django.contrib.auth.models import User
import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm
from .models import Like

# Create your views here.
# 这里别看！
# 文章列表
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    tag = request.GET.get('tag')
    column = request.GET.get('column')
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''
    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in = [tag])
    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column = column)
    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    # 每页显示一篇文章
    paginator = Paginator(article_list, 3)
    # 获取url中的页码
    page = request.GET.get('page')
    # 将paginator对象相应的页码内容返回给articles
    articles = paginator.get_page(page)

    # 需要传递给模板的对象
    context = {'articles':articles, 'order':order, 'search':search, 'tag':tag, 'column':column}
    # 使用快捷方式render()函数
    return render(request, 'article/list.html', context)

# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    # article = ArticlePost.objects.get(id = id)
    article = get_object_or_404(ArticlePost, id = id)
    # 取出文章评论
    comments = Comment.objects.filter(article = id)
    # 取出评论表单
    comment_form = CommentForm()
    # 浏览量+1
    article.total_views += 1
    article.save(update_fields = ['total_views'])
    # 将markdown语法渲染成html样式
    # article.body = markdown.markdown(article.body,
    #                                  extensions = [
    #                                      'markdown.extensions.extra',
    #                                      'markdown.extensions.codehilite',
    #                                      # 目录扩展
    #                                      'markdown.extensions.toc'
    #                                  ])
    md = markdown.Markdown(
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    # 需要传递给模板的对象
    context = {'article':article, 'toc':md.toc, 'comments':comments, 'comment_form':comment_form}
    return render(request, 'article/detail.html', context)

# 写文章
@login_required(login_url = '/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit = False)
            new_article.author = User.objects.get(id = request.user.id)
            # 保存栏目
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id = request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            article_post_form.save_m2m()
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 获取所有栏目
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = { 'article_post_form': article_post_form, 'columns':columns }
        # 返回模板
        return render(request, 'article/create.html', context)

# 删文章
@login_required(login_url = '/userprofile/login/')
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    if article.author_id != request.user.id:
        return HttpResponse('你没有权限删除此文章！')
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")

# 安全删除文章
@login_required(login_url = '/userprofile/login/')
def article_safe_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    if article.author_id != request.user.id:
        return HttpResponse('你没有权限删除此文章！')
    if request.method == 'POST':
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许POST请求')

# 修改文章
@login_required(login_url = '/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的文章对象
    article = ArticlePost.objects.get(id = id)
    if article.author_id != request.user.id:
        return HttpResponse('你没有权限更新此文章！')
    # 判断用户是否为post提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的title、body
            article.title = request.POST['title']
            article.body = request.POST['body']
            # 保存栏目
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            # 保存新的标题图
            article.avatar = article_post_form.cleaned_data['avatar']
            print(article_post_form.cleaned_data)
            print(request.POST)
            article.save()
            # 完成后返回到修改后的文章详情
            return redirect('article:article_detail', id = id)
        else:
            return HttpResponse('表单内容有误，请重新填写！')
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article':article, 'article_post_form':article_post_form, 'columns':columns}
        return render(request, 'article/update.html', context)

# 点赞类视图
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id = kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')

# 从这里开始才是
class Article:
    # 文档的创建
    @staticmethod
    def article_create(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')
            userid = data.get('userid')
            articlepost = ArticlePost.objects.create(author_id = userid, title = title, body = content, last_updater = userid)
            articlepost.save()
            return JsonResponse({
                "status":0,
                "articleid":articlepost.id
            })
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })
    # 文档的修改
    @staticmethod
    def article_update(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            articleid = data.get('articleid')
            userid = data.get('userid')
            title = data.get('title')
            content = data.get('content')
            articlepost = ArticlePost.objects.get(id = articleid)
            articlepost.title = title
            articlepost.body = content
            articlepost.last_updater = userid
            articlepost.save()
            return JsonResponse({
                "status": 0,
                "articleid": articlepost.id
            })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })
    # 文档查看
    @staticmethod
    def article_get(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            articleid = data.get('articleid')
            article = ArticlePost.objects.get(id = articleid)
            title = article.title
            content = article.body
            author = article.author
            created = article.created
            last_updater = User.objects.get(id = article.last_updater).username
            update_time = article.updated
            is_in_garbage = article.is_in_garbage
            return JsonResponse({
                "status":0,
                "title":title,
                "content":content,
                "author":author.username,
                "created_time":created,
                "last_updater":last_updater,
                "updated_time":update_time,
                "is_in_garbage":is_in_garbage
            })
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })
    # 文档删除，根据实际情况进行进入回收站或者彻底删除
    @staticmethod
    def article_remove(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            articleid = data.get('articleid')
            article = ArticlePost.objects.get(id = articleid)
            if article.is_in_garbage:
                article.delete()
                return JsonResponse({
                    "status":0,
                    "message":"彻底删除"
                })
            else:
                article.is_in_garbage = True
                article.save()
                return JsonResponse({
                    "status":0,
                    "message":"移入回收站"
                })
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })
    # 文档恢复
    @staticmethod
    def article_recover(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            articleid = data.get('articleid')
            article = ArticlePost.objects.get(id = articleid)
            article.is_in_garbage = False
            article.save()
            return JsonResponse({
                "status":0,
                "message":"success"
            })
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })

    # 文档收藏或取消收藏
    @staticmethod
    def article_like(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            userid = data.get('userid')
            articleid = data.get('articleid')
            is_like = data.get('islike')
            if is_like == 0:
                likes = Like.objects.filter(liker_id = userid, liked_id = articleid)
                for like in likes:
                    like.delete()
                return JsonResponse({
                    "status":0,
                    "message":"dislike success"
                })
            else:
                like = Like.objects.create(liker_id = userid, liked_id = articleid)
                like.save()
                return JsonResponse({
                    "status": 0,
                    "message": str(like)
                })
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })






