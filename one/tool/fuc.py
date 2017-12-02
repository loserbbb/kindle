import re 
import hashlib
from one import models
import threading
from datetime import timedelta
from datetime import datetime
from datetime import date
from django.core.mail import EmailMessage


def session(userId, content):
    if content == '帮助':
        reply = '''
        请严格按照步骤，否则将不能成功推书：
        1. 在亚马逊中国www.amazon.cn登陆您的账户，在我的账户->管理我的内容和设备->设置->认可的发件人电子邮箱列表 中添加认可的电子邮箱为 xiaobin@weijb.xin
        2. 对公众号发送"绑定邮箱xxxxx@kindle.cn"邮箱为您的Kindle推送邮箱，可以在kindle->设置->我的账户->【发送至Kindle】的电子邮件地址 查看
        3. 完成绑定之后，对公众号发送书名查询图书
        4. 对公众号发送"推送XX" (XX是“书号”)来推送图书到您的kindle 
        5. 发送"#"可以无限推送书籍

=========================
        6. 推送到下载邮箱教程：对公众号发送“绑定下载邮箱xxxx@xx.xx”（该邮箱为要接受书籍的个人邮箱，例如qq邮箱），然后发送“下载XX”(XX是“书号”),书籍将会发送到您的个人邮箱，下载邮件附件，然后将文件通过USB接口复制到kindle的Document文件夹中
        '''
        return reply
    pattern = re.compile(r'绑定邮箱(.+@.+\.\w+)', re.I)
    match = re.match(pattern, content)
    if match:
        email = match.group(1)
        pattern = re.compile(r'.+@kindle.cn', re.I)
        if not re.match(pattern, email):
            return "请检查邮箱格式！回复“帮助”可以获取推送教程"
        try:
            fans = models.Fans.objects.get(fansid=userId)
            fans.email = email
            fans.lastpush = date.today()
            fans.save()
            return '邮箱更换成功'
        except:
            fans = models.Fans(fansid=userId, email=email)
            fans.save()
            return '绑定成功，您可以往您的kindle中推送书籍了,回复“帮助”查看推送教程'

    elif re.match('绑定下载邮箱(.+@.+\.\w+)', content):
        email = re.match('绑定下载邮箱(.+@.+\.\w+)', content).group(1)
        try:
            fans = models.Fans.objects.get(fansid=userId)
            fans.downloademail = email 
            fans.lastdownload = date.today()
            fans.save()
            return '下载邮箱更换成功'
        except:
            fans = models.Fans(fansid=userId, downloademail=email)
            fans.save()
            return '绑定成功，你可以往你邮箱中发送书籍并下载，然后通过usb接口传输到kindle中,回复“帮助”查看下载教程'

    elif re.match('.+@.+\.\w+', content):
        return '请按格式来绑定邮箱，回复"帮助"查看'

    elif content == '#':
        vipreply = '输入以下命令获取服务：\n#1 vip价格\n#2 购买：加微信XE3554\n#3 查询vip到期时间及天数'
        return vipreply

    elif re.match('#\d', content):
        if content[1] == '1':
            return '38.8元/年\t\t   无限推送/天\n66.6元/两年\t\t无限推送/天\n88.8元/永久\t\t无限推送/天'
        elif content[1] == '2':
            return '购买:加微信XE3554'
        elif content[1] == '3':
            fans = models.Fans.objects.get(fansid=userId)
            if fans.rank == 4:
                return '到期时间：永久'
            if fans.rank != 0:
                delta = fans.deadline - date.today()
                return '到期时间：{}\n剩余：{}天'.format(fans.deadline, delta.days)
            else:
                return '您还不是vip,请先购买'
        else:
            return '指令错误'

    elif re.match('^###\d$', content):
        if content[3] in ['2', '3', '4']:
            source = datetime.now().timestamp()
            md5 = hashlib.md5()
            md5.update(str(source).encode('utf-8'))
            code = md5.hexdigest()
            models.Activationcode(code=code, rank=int(content[3])).save()
            return code
        else:
            return '指令超范围'

    elif re.match('激活码.+', content):
        try:
            code = models.Activationcode.objects.get(code=re.match('激活码(.+)', content).group(1))
            try:
                fans = models.Fans.objects.get(fansid=userId)
            except:
                return '请先绑定邮箱'
            price = {'2': 38.8, '3': 66.6, '4': 88.8}
            if fans.deadline is None or fans.deadline <= date.today():
                startdate = date.today()
            else:
                startdate = fans.deadline
            if code.rank == 2:
                fans.deadline = startdate + timedelta(days=366)
                fans.rank = 2
            elif code.rank == 3:
                fans.deadline = startdate + timedelta(days=731)
                fans.rank = 3
            elif code.rank == 4:
                fans.rank = 4
            fans.save()
            models.Count(rank=code.rank, price=price[str(code.rank)]).save()
            code.delete()
            return '升级vip成功'
        except:
            return '激活码错误'
    elif re.match('下载\d+', content):
        try:
            rep = '今日的下载次数已用完，明天再来吧\n回复“#”进入vip菜单'
            fans = models.Fans.objects.get(fansid=userId)
            if fans.lastdownload != date.today():
                fans.downloadtimes = 0
                fans.lastdownload = date.today()
            if fans.rank not in [0, 4] and fans.deadline <= date.today():
                fans.rank = 0
                fans.save()
            if fans.rank == 0 and fans.downloadtimes >= 0:
                return rep 
                #return '由于近期推送人数较多，服务器压力较大，很多用户无法收到书籍，将进行为期一周的升级，普通用户期间无法推送，vip用户正常使用,回复“#”获取vip'
            bookid = re.match('下载(\d+)', content).group(1)
            book = models.Book.objects.get(id=int(bookid))
            fans.downloadtimes += 1
            push = threading.Thread(target=pushbook, name='pushbook', args=(book.bookpath, fans.downloademail))
            push.start()
            models.Pushlist(bookname=book.bookname, bookpath=book.bookpath, usermail=fans.downloademail).save()
            fans.save()
            return '推送到下载邮箱成功,如果没有推送成功，请联系管理员XE3554或发送信息到xiaobin@weijb.xin'
        except:
            return '推送到下载邮箱失败，请先绑定下载邮箱或者核对书号是否正确，回复“帮助”获取绑定下载邮箱教程'

    elif re.match('推送\d+', content):
        try:
            rep = '今日的推送次数已用完，明天再来吧\n回复“#”进入vip菜单'
            fans = models.Fans.objects.get(fansid=userId)
            if fans.lastpush != date.today():
                fans.times = 0
                fans.lastpush = date.today()
            if fans.rank not in [0, 4] and fans.deadline <= date.today():
                fans.rank = 0
                fans.save()
            if fans.rank == 0 and fans.times >= 1:
                return rep
                #return '由于近期推送人数较多，服务器压力较大，很多用户无法收到书籍，将进行为期一周的升级，普通用户期间无法推送，vip用户正常使用，回复“#”获取vip'
            bookid = re.match('推送(\d+)', content).group(1)
            book = models.Book.objects.get(id=int(bookid))
            if re.match('.+\.azw3?', book.bookpath) or re.match('.+\.epub', book.bookpath):
                return 'azw3,epub,azw格式的书籍亚马逊服务器不支持转格式，不能直接推送到kindle,请选择推送其他格式的书籍或者推送到下载邮箱，回复“帮助”查看推送到下载邮箱教程'
            fans.times += 1
            push = threading.Thread(target=pushbook, name='pushbook', args=(book.bookpath, fans.email))
            push.start()
            models.Pushlist(bookname=book.bookname, bookpath=book.bookpath, usermail=fans.email).save()
            fans.save()
            return '推送成功,如果没有推送成功，请联系管理员XE3554或发送信息到xiaobin@weijb.xin'
        except Exception as e:
            # return str(e)
            return '推送失败，请先绑定邮箱或者核对书号是否正确,回复“帮助”获取绑定邮箱教程'
    elif re.match('推送.+', content):
        return '推送格式错误\n请回复"推送XX" (XX是要推送的书号)\n 或回复"帮助"查看推送教程'
    else:
        try:
            booklist = models.Book.objects.filter(bookpath__icontains=content)[0: 50]
            a = '查询到以下书籍:\n=============\n'
            for book in booklist:
                a += '%s\n书号: %s\n' % (book.bookname, book.id)
                if len(a.encode('utf-8')) > 1800:
                    break
            if len(booklist) == 0:
                a += '未查到相关书籍，请更换关键词搜索\n'
            a += '==============\n回复 “推送XX”（XX为书号）即可推送到kindle\n*注意*:azw3,epub格式的图书不支持直接推送到Kindle,请选择推送到下载邮箱，回复“帮助”查看'
            return a 
        except:
            return '没有查询到相关书籍'


def pushbook(bookpath, toemail):
    email = EmailMessage(subject='kindlepush', body='您的书到', from_email='kindle@weijb.xin', to=[toemail])
#    email.attach_file(bookpath, mimetype='application/x-mobi')
    if re.match(r'.+\.txt$', bookpath):
        email.attach_file(bookpath, mimetype='application/x-mobi')
    else:
        email.attach_file(bookpath)
    email.send(fail_silently=True)
 

def eventreply(userId, event):
    if event == 'subscribe':
        reply = '''
        请严格按照步骤，否则将不能成功推书：
        1. 在亚马逊中国www.amazon.cn登陆您的账户，在我的账户->管理我的内容和设备->设置->认可的发件人电子邮箱列表 中添加认可的电子邮箱为 xiaobin@weijb.xin
        2. 对公众号发送"绑定邮箱xxxxx@kindle.cn"邮箱为您的Kindle推送邮箱，可以在kindle->设置->我的账户->【发送至Kindle】的电子邮件地址 查看
        3. 完成绑定之后，对公众号发送书名查询图书
        4. 对公众号发送"推送XX" (XX是书号)来推送图书到您的kindle
        '''
        return reply 
    else:
        return ''
