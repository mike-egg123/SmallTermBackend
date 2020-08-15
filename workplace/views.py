from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json
# Create your views here.
from workplace.models import *
from article.models import ArticlePost, Like
from userprofile.models import Profile

# 修改处：
# 1、把表Users删了直接替换成django内建的User，不然如果Users表是空的，则无法进行团队的操作，而一开始Users表必然是空的
# 2、将所有的从前端获取的参数名进行了规范化
# 3、myteam中向前端多返回一个teamid
# 4、感觉踢人和退出团队的两个函数一模一样
# 加入的团队（不包括创建的）
def myjointeam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        usr = User.objects.get(id=uid)
        res = usr.user.all()
        reslist = []
        for tm in res:
            if tm.tcreateuser != usr:
                temp = {'teamname':tm.tname, 'creator':tm.tcreateuser.username, 'tnum':tm.tnum,
                       'createtime':tm.tcreatetime.strftime('%Y-%m-%d %H:%I:%S'), 'teamid':tm.tid
                        }
                reslist.append(temp)
        return JsonResponse(reslist, safe = False)

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })
def myjointeamYi(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": 1,
                "message": "请先登录"
            })
        uid = request.user.id
        usr = User.objects.get(id=uid)
        res = usr.user.all()
        reslist = []
        for tm in res:
            if tm.tcreateuser != usr:
                temp = {'teamname':tm.tname, 'creator':tm.tcreateuser.username, 'tnum':tm.tnum,
                       'createtime':tm.tcreatetime.strftime('%Y-%m-%d %H:%I:%S'), 'teamid':tm.tid
                        }
                reslist.append(temp)
        return JsonResponse(reslist, safe = False)
    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

# 创建的团队
def mycreateteam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        usr = User.objects.get(id=uid)
        res = usr.user.all()
        reslist = []
        for tm in res:
            if tm.tcreateuser == usr:
                temp = {'teamname':tm.tname, 'creator':tm.tcreateuser.username, 'tnum':tm.tnum,
                       'createtime':tm.tcreatetime.strftime('%Y-%m-%d %H:%I:%S'), 'teamid':tm.tid
                        }
                reslist.append(temp)
        return JsonResponse(reslist, safe = False)

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

# 创建的团队（异步）
def mycreateteamYi(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({
                "message":"请先登录"
            })
        uid = request.user.id
        usr = User.objects.get(id=uid)
        res = usr.user.all()
        reslist = []
        for tm in res:
            if tm.tcreateuser == usr:
                temp = {'teamname':tm.tname, 'creator':tm.tcreateuser.username, 'tnum':tm.tnum,
                       'createtime':tm.tcreatetime.strftime('%Y-%m-%d %H:%I:%S'), 'teamid':tm.tid
                        }
                reslist.append(temp)
        return JsonResponse(reslist, safe = False)

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })


#创建团队
def createteam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        teamname = data.get("teamname")
        uid = data.get("userid")
        if teamname is not None:
            res = Team.objects.filter(tname=teamname)
            if res.exists():
                return JsonResponse({
                    "status": 2,
                    "message": "该小组名已存在"
                })
            else:
                team = Team.objects.create(tname=teamname, tcreateuser_id=uid, tnum=1)
                memlist = []
                memlist.append(User.objects.get(id=uid))
                team.tmem.add(*memlist)
                team.save()
                return JsonResponse({
                    "status": 0,
                    "message": "Create team success"
                })


    else:
        return JsonResponse({
            "status": 1,
            "message": "error method"
        })

#解散团队
def disband(request):
    if request.method == "POST":
        data = json.loads(request.body)
        teamid = data.get("teamid")
        if teamid is not None:
            res = Team.objects.filter(tid=teamid).first()
            res.tmem.clear()
            res.delete()
            return JsonResponse({
                "status": 0,
                "message": "Disband team success"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "error method"
        })

#退出团队
def exitteam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        teamid = data.get("teamid")
        uid = data.get("userid")
        if teamid is not None:
            res = Team.objects.filter(tid=teamid).first()
            user = User.objects.filter(id=uid).first()
            res.tmem.remove(user)
            res.tnum = res.tnum - 1
            res.save()
            return JsonResponse({
                "status": 0,
                "message": "Exit team success"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "error method"
        })

#踢人
def outteam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        teamid = data.get("teamid")
        userid = data.get("userid")
        if teamid is not None:
            res = Team.objects.filter(tid=teamid).first()
            user = User.objects.filter(id=userid).first()
            res.tmem.remove(user)
            res.tnum = res.tnum - 1
            res.save()
            return JsonResponse({
                "status": 0,
                "message": "Out team success"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "error method"
        })

#加入团队
def jointeam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        teamid = data.get("teamid")
        uid = data.get("userid")
        tm = Team.objects.get(tid=teamid)
        usr = User.objects.get(id=uid)
        tm.tmem.add(usr)
        tm.tnum = tm.tnum+1
        tm.save()
        return JsonResponse({
            "status": 0,
            "message": "加入成功"
        })

    else:
        return JsonResponse({
            "status": 1,
            "message": "error method"
        })

# 以下为新增
# 查找团队成员
def getteammember(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teamid = data.get('teamid')
        team = Team.objects.get(tid = teamid)
        members = team.tmem.all()
        mem_list = []
        for member in members:
            mem_dict = {}
            profile = Profile.objects.get(user = member)
            mem_dict["userid"] = member.id
            mem_dict["username"] = member.username
            mem_dict["avatar"] = "http://182.92.239.145" + str(profile.avatar.url)
            mem_list.append(mem_dict)
        return JsonResponse(mem_list, safe = False)

# 查找该团队中所有权限为1或2的文档
def getallarticles(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                "message":"请先登录"
            })
        data = json.loads(request.body)
        teamid = data.get('teamid')
        user = request.user
        team = Team.objects.get(tid=teamid)
        members = team.tmem.all()
        article_list = []
        for member in members:
            articles = ArticlePost.objects.filter(author = member)
            for article in articles:
                if article.permission != 0:
                    article_dict = {}
                    article_dict['articleid'] = article.id
                    article_dict['title'] = article.title
                    article_dict['author'] = member.username
                    article_dict['created'] = article.created
                    if Like.objects.filter(liker = user, liked = article).exists():
                        article_dict['islike'] = True
                    else:
                        article_dict['islike'] = False
                    article_list.append(article_dict)
        return JsonResponse(article_list, safe = False)


