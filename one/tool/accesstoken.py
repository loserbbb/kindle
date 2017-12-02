from one.models import Accesskey
from datetime import datetime
from datetime import timedelta
import requests
import json
def getaccesskey():
    accesskey = Accesskey.objects.get(id=1)
    if datetime.now().timestamp() - accesskey.gettime > 7000:
        r = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxf363b98a8066f449&secret=b8d25900be914e70b48520065ef295bc')
        print(r.text)
        d = json.loads(r.text)
        key = d['access_token']
        accesskey.key = key
        accesskey.gettime = datetime.now().timestamp()
        accesskey.save()
        return key
    else:
        return accesskey.key
