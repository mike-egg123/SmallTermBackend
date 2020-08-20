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

# 拥有的所有团队
def myallteam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        usr = User.objects.get(id=uid)
        reslist = []
        if usr.user:
            res = usr.user.all()
            for tm in res:
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
            Permissions.objects.filter(tid=teamid).delete()
            Prepermission.objects.filter(tid=teamid).delete()
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
        tm = Team.objects.get(tid=teamid)
        if teamid is not None:
            res = Team.objects.filter(tid=teamid).first()
            user = User.objects.filter(id=uid).first()
            if res.tnum == 2:
                ppmslist = Permissions.objects.filter(tid=teamid, uid=user).all()  #只保留团队创建者的权限设置
                for ppms in ppmslist:
                    Prepermission.objects.create(state=ppms.state, tid=teamid, did=ppms.did)
            Permissions.objects.filter(tid=teamid, uid=user).delete() #别人给自己的文档权限
            mydoc = ArticlePost.objects.filter(author=user).all()
            for doc in mydoc:
                Permissions.objects.filter(tid=teamid, did=doc.id).delete() #自己给别人的文档权限
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
            if res.tnum == 2:
                ppmslist = Permissions.objects.filter(tid=teamid, uid=user).all()
                for ppms in ppmslist:
                    Prepermission.objects.create(state=ppms.state, tid=teamid, did=ppms.did)
            Permissions.objects.filter(tid=teamid, uid=user).delete()
            mydoc = ArticlePost.objects.filter(author=user).all()
            for doc in mydoc:
                Permissions.objects.filter(tid=teamid, did=doc.id).delete()  # 自己给别人的文档权限
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
        if tm.tnum == 2: #团队的第一个加入成员，获得预设的文档权限
            ppmslist = Prepermission.objects.filter(tid=teamid).all()
            for ppms in ppmslist:
                Permissions.objects.create(state=ppms.state, tid=teamid, uid=usr, did=ppms.did)
            Prepermission.objects.filter(tid=teamid).delete()
        else: #复制团队其他成员的文档权限
            pmsist = Permissions.objects.filter(tid=teamid).all()
            for pms in pmsist:
                Permissions.objects.create(state=pms.state, tid=teamid, uid=usr, did=pms.did)
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
            if profile.avatar:
                mem_dict["avatar"] = "http://182.92.239.145" + str(profile.avatar.url)
            else:
                mem_dict['avatar'] = " "
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

# 查询团队信息
def getteaminfo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teamid = data.get('teamid')
        team = Team.objects.get(tid = teamid)
        if team:
            return JsonResponse({
                "teamid":teamid,
                "teamname":team.tname,
                "creator":team.tcreateuser.username,
                "tnum":team.tnum,
                "createtime":team.tcreatetime
            })
        else:
            return JsonResponse({
                "message":"查询的团队不存在"
            })
    else:
        return JsonResponse({
            "message":"error method"
        })

#设置（修改）文档权限
def setpermission(request):
    if request.method == "POST":
        data = json.loads(request.body)
        state = data.get("state") ##权限值 0为私有 1为团队可见 2为团队可见可改
        uid = data.get("userid") #用户id
        did = data.get("articleid") #文档id
        teamlist = []
        teamlist = data.get("teamlist") #如果 state>=1 需要提交team的id列表
        #如果设置的团队为空，需要先将权限暂存，待第一个用户加入，修改权限表，删除暂存
        Permissions.objects.filter(did_id=did).delete()
        Permissions.objects.create(state=0, uid_id=uid, did_id=did, tid=-1)
        if state == 1:
            for tid in teamlist:
                tm = Team.objects.get(tid=tid)
                if tm.tnum == 1:
                    Prepermission.objects.create(state=1, did_id=did, tid=tid)
                    continue
                for usr in tm.tmem.all():
                    if usr.id == uid:
                        continue
                    Permissions.objects.create(state=1, uid=usr, did_id=did, tid=tid)

        if state == 2:
            for tid in teamlist:
                tm = Team.objects.get(tid=tid)
                if tm.tnum == 1:
                    Prepermission.objects.create(state=2, did_id=did, tid=tid)
                    continue
                for usr in tm.tmem.all():
                    if usr.id == uid:
                        continue
                    Permissions.objects.create(state=2, uid=usr, did_id=did, tid=tid)

        return JsonResponse({
            "status": 1,
            "message": "设置成功"
        })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#查询团队文档
def getteamdoc(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid= data.get("teamid")
        uid = data.get("userid")
        doclist = []
        pmsist = Permissions.objects.filter(tid=tid).all()
        for pms in pmsist:
            doc = pms.did_id
            if doc not in doclist:
                doclist.append(doc)
        reslist = []
        for docid in doclist:
            state = 0
            p = Permissions.objects.filter(did=docid, uid=uid, tid=-1)
            if len(p) == 1:
                state = 0
            else:
                state = Permissions.objects.filter(did=docid, uid=uid, tid=tid).first().state
            article = ArticlePost.objects.get(id = docid)
            if article.is_in_garbage == False:
                res = {'articleid':docid,
                    'title':ArticlePost.objects.get(id=docid).title,
                       'author':ArticlePost.objects.get(id=docid).author.username,
                       'state':state,
                       'created':ArticlePost.objects.get(id = docid).created}
                reslist.append(res)
        return JsonResponse(reslist, safe=False)
    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#查找文档（全局搜索的文档部分）
def searchdoc(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        keyword = data.get("keyword")
        doclist = []
        pmsist = Permissions.objects.filter(uid=uid).all()
        for pms in pmsist:
            doc = pms.did_id
            if doc not in doclist:
                doclist.append(doc)
        reslist = []
        for docid in doclist:
            doc = ArticlePost.objects.get(id=docid)
            title = doc.title
            if title.find(keyword) != -1 and doc.is_in_garbage==False:
                res = {'articleid': docid,
                       'title': title,
                       'author': ArticlePost.objects.get(id=docid).author.username,
                       'state': Permissions.objects.filter(did=docid, uid=uid).first().state
                        }
                reslist.append(res)
        return JsonResponse(reslist, safe=False)
    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#查找团队（全局搜索的团队部分）
def searchteam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        keyword = data.get("keyword")
        usr = User.objects.get(id=uid)
        teamlist = []
        teamlist = Team.objects.filter(tname__icontains=keyword).all()
        reslist = []
        for tm in teamlist:
            state = 0 #状态值：自己创建为0，加入的为1，未加入的为2
            if tm.tcreateuser == usr:
                state = 0
            elif usr in tm.tmem.all():
                state = 1
            else:
                state = 2
            res = {'teamid': tm.tid,
                   'teamname': tm.tname,
                   'teamcreator': tm.tcreateuser.username,
                   'state': state
                    }
            reslist.append(res)
        return JsonResponse(reslist, safe=False)
    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

# 查询权限
def getpermission(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        aid = data.get("articleid")
        state = 0
        article = ArticlePost.objects.get(id=aid)
        if article.author.id == uid :
            return JsonResponse({
                "state": state
            })
        if len(Permissions.objects.filter(uid_id=uid, did_id=aid).all()) >= 1:
            state = Permissions.objects.filter(uid_id=uid, did_id=aid).first().state
        else:
            state = 500
        return JsonResponse({
            "state": state
        })
    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#查询权限设置
def getpermissionsetting(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        aid = data.get("articleid")
        state = 0
        teamlist = []
        res = Permissions.objects.filter(did_id=aid).all()
        if len(res) == 1:
            state = 0
            return JsonResponse({
                "state": state,
                "teamlist": teamlist
            })
        else:
            for pms in res :
                if pms.state == 0:
                    continue
                state = pms.state
                break

        for pms in res:
            if pms.tid == -1:
                continue
            teamname = Team.objects.get(tid=pms.tid).tname
            if teamname not in teamlist:
                teamlist.append(teamname)
        return JsonResponse({
            "state": state,
            "teamlist":teamlist
        })
    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })


