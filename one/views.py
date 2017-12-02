from django.shortcuts import render
from django.shortcuts import HttpResponse
import hashlib
from .tool import reply, receive, fuc
# Create your views here.


def handle(request):
    if request.method == 'GET':
        try:
            signature = request.GET.get('signature')
            timestamp = request.GET.get('timestamp')
            nonce = request.GET.get('nonce')
            echostr = request.GET.get('echostr')
            token = 'kindlefreepush'

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            for i in list:
                sha1.update(bytes(i, encoding='utf-8'))
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return HttpResponse(echostr)
            else:
                return HttpResponse('')
        except:
            return HttpResponse('')
    elif request.method == 'POST':
        try:
            webData = request.body
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUserName = recMsg.ToUserName
                content = fuc.session(toUser, recMsg.Content)
                replyMsg = reply.TextMsg(toUser, fromUserName, content)
                return HttpResponse(replyMsg.send())
            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'event':
                toUser = recMsg.FromUserName
                fromUserName = recMsg.ToUserName
                content = fuc.eventreply(toUser, recMsg.Event)
                replyMsg = reply.TextMsg(toUser, fromUserName, content)
                return HttpResponse(replyMsg.send())
            else:
                return HttpResponse('success')
        except Exception as e:
            return HttpResponse(e)
    else:
        HttpResponse('hello')

