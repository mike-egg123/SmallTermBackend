from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json

from workplace.models import *
from article.models import ArticlePost, Like
from userprofile.models import Profile
from .models import *

# Create your views here.

#查找邀请用户
def getuser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        tid = data.get("teamid")
        username = data.get("username")
        res = len(User.objects.filter(username=username).all())
        if res == 1:
            tm = Team.objects.get(tid=tid)
            usr = User.objects.get(username=username)
            if usr not in tm.tmem.all():
                return JsonResponse({
                    "status": 1,
                    "username":usr.username,
                    "userid":usr.id
                })
            else:
                return JsonResponse({
                    "status": 2,
                    "message": username+" is already in the team"
                })
        else:
            return JsonResponse({
                "status": 2,
                "message": "no user named "+username
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#邀请用户加入团队
def invite(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid = data.get("teamid")
        tuid = data.get("inviteduserid")
        uid = data.get("userid")
        flag = len(Teammessage.objects.filter(messagetype=1,tuid_id=tuid, tid_id=tid).all()) #重复邀请只保留最近记录
        if flag>=1:
            Teammessage.objects.filter(messagetype=1, tuid_id=tuid, tid_id=tid).delete()
        Teammessage.objects.create(messagetype=1, tid_id=tid, uid_id=uid,
                  message=User.objects.get(id=uid).username +" 邀请您加入团队【"+ Team.objects.get(tid=tid).tname+"】",
                                   tuid_id=tuid)
        return JsonResponse({
                "message": "send message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#同意邀请生成消息通知
def agreeinvitation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid = data.get("teamid")
        tuid = data.get("inviteuserid")
        uid = data.get("userid")
        tm = Team.objects.get(tid=tid)
        usr = User.objects.get(id=uid)
        if usr in tm.tmem.all():
            return JsonResponse({
                "status": 2,
                "message": "You are already in the team"
            })
        else:
            Teammessage.objects.create(messagetype=3, tid=tm, uid_id=uid,
                      message=usr.username +" 同意了您的邀请，加入了团队【"+ tm.tname+"】",
                                       tuid_id=tuid)
            return JsonResponse({
                    "message": "send message success"
                })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })


#拒绝邀请
def refuseinvitation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid = data.get("teamid")
        tuid = data.get("inviteuserid")
        uid = data.get("userid")
        Teammessage.objects.create(messagetype=2, tid_id=tid, uid_id=uid,
                  message=User.objects.get(id=uid).username +" 拒绝加入您的团队【"+ Team.objects.get(tid=tid).tname+"】",
                                   tuid_id=tuid)
        return JsonResponse({
                "message": "send message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#申请加入团队
def apply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid = data.get("teamid")
        uid = data.get("userid")
        flag = len(Teammessage.objects.filter(messagetype=4, uid_id=uid, tid_id=tid).all()) #重复申请只保留最近记录
        if flag>=1:
            Teammessage.objects.filter(messagetype=4, uid_id=uid, tid_id=tid).delete()
        tm = Team.objects.get(tid=tid)
        Teammessage.objects.create(messagetype=4, tid_id=tid, uid_id=uid,
                  message=User.objects.get(id=uid).username +" 申请加入您的团队【"+ tm.tname+"】",
                                   tuid=tm.tcreateuser)
        return JsonResponse({
                "message": "send message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#同意申请生成消息通知
def agreeapply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid = data.get("teamid")
        tuid = data.get("applyuserid")
        uid = data.get("userid")
        tm = Team.objects.get(tid=tid)
        usr = User.objects.get(id=tuid)
        if usr in tm.tmem.all():
            return JsonResponse({
                "status": 2,
                "message": "The user is already in the team"
            })
        else:
            Teammessage.objects.create(messagetype=5, tid=tm, uid_id=uid,
                      message=User.objects.get(id=uid).username +" 同意了您加入团队【"+ tm.tname+"】的申请",
                                       tuid=usr)
            return JsonResponse({
                    "message": "send message success"
                })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#拒绝申请
def refuseapply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid = data.get("teamid")
        tuid = data.get("applyuserid")
        uid = data.get("userid")
        Teammessage.objects.create(messagetype=6, tid_id=tid, uid_id=uid,
                  message=User.objects.get(id=uid).username +" 拒绝了您加入团队【"+ Team.objects.get(tid=tid).tname+"】的申请",
                                   tuid_id=tuid)
        return JsonResponse({
                "message": "send message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })


#踢人生成消息通知
def outteammessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid = data.get("teamid")
        tuid = data.get("outuserid")
        uid = data.get("userid")
        Teammessage.objects.create(messagetype=7, tid_id=tid, uid_id=uid,
                  message=User.objects.get(id=uid).username +" 将您请出了团队【"+ Team.objects.get(tid=tid).tname+"】",
                                   tuid_id=tuid)
        return JsonResponse({
                "message": "send message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#退出团队生成消息通知
def exitteammessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tid = data.get("teamid")
        uid = data.get("userid")
        Teammessage.objects.create(messagetype=8, tid_id=tid, uid_id=uid,
                  message=User.objects.get(id=uid).username +" 退出了团队【"+ Team.objects.get(tid=tid).tname+"】",
                                   tuid=Team.objects.get(tid=tid).tcreateuser)
        return JsonResponse({
                "message": "send message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })


#忽略（已读）团队消息通知
def solveteammessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mid = data.get("messageid")
        Teammessage.objects.filter(id=mid).delete()
        return JsonResponse({
                "message": "solve message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })


#评论生成消息通知
def commentmessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        aid = data.get("articleid")
        uid = data.get("userid")
        Commentmessage.objects.create(aid_id=aid, uid_id=uid,
            message=User.objects.get(id=uid).username +" 评论了您的文档《"+ ArticlePost.objects.get(id=aid).title+"》",
                                   tuid=ArticlePost.objects.get(id=aid).author)
        return JsonResponse({
                "message": "send message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#评论消息通知处理
def solvecommentmessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mid = data.get("messageid")
        Commentmessage.objects.filter(id=mid).delete()
        return JsonResponse({
                "message": "solve message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#接收消息
def getmessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        msglist= []
        mres = Teammessage.objects.filter(tuid_id=uid).all()
        for res in mres:
            record = {
                "messageid":res.id,
                "messagetype":res.messagetype,
                "userid":res.uid.id,
                "username":res.uid.username,
                "teamid":res.tid.tid,
                "teamname":res.tid.tname,
                "message":res.message,
                "time":res.time
            }
            msglist.append(record)
        cres = Commentmessage.objects.filter(tuid_id=uid).all()
        for res in cres:
            record = {
                "messageid": res.id,
                "messagetype": res.messagetype,
                "userid":res.uid.id,
                "username":res.uid.username,
                "articleid":res.aid.id,
                "title":res.aid.title,
                "message":res.message,
                "time":res.time
            }
            msglist.append(record)
        return JsonResponse(msglist, safe=False)

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })
