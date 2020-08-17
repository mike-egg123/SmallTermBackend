from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json

from userprofile.models import Profile
from .models import *

#发送私信
def sendmessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        message = data.get("message")
        tuid = data.get("touserid")
        Message.objects.create(uid_id=uid, message=message, tuid_id=tuid)
        return JsonResponse({
                "message": "send message success"
            })
    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })

#接收私信
def getmessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data.get("userid")
        msglist= []
        mres = Message.objects.filter(tuid_id=uid).all()
        for res in mres:
            record = {
                "messageid":res.id,
                "userid":res.uid.id,
                "username":res.uid.username,
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

#删除私信
def deletemessage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mid = data.get("messageid")
        Message.objects.filter(id=mid).delete()
        return JsonResponse({
                "message": "delete message success"
            })

    else:
        return JsonResponse({
            "status": 0,
            "message": "error method"
        })