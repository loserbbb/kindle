import xml.etree.ElementTree as ET


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlDate = ET.fromstring(web_data)
    msg_type = xmlDate.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlDate)
    elif msg_type == 'image':
        return ImageMsg(xmlDate)
    elif msg_type == 'event':
        return EventMsg(xmlDate)


class Msg:
    def __init__(self, xmlDate):
        self.ToUserName = xmlDate.find('ToUserName').text 
        self.FromUserName = xmlDate.find('FromUserName').text 
        self.CreateTime = xmlDate.find('CreateTime').text 
        self.MsgType = xmlDate.find('MsgType').text 


class TextMsg(Msg):
    def __init__(self, xmlDate):
        Msg.__init__(self, xmlDate)
        self.Content = xmlDate.find('Content').text
        self.MsgId = xmlDate.find('MsgId').text 


class ImageMsg(Msg):
    def __init__(self, xmlDate):
        Msg.__init__(self, xmlDate)
        self.PicUrl = xmlDate.find('PicUrl').text 
        self.MediaId = xmlDate.find('MediaId').text 
        self.MsgId = xmlDate.find('MsgId').text 


class EventMsg(Msg):
    def __init__(self, xmlDate):
        Msg.__init__(self, xmlDate)
        self.Event = xmlDate.find('Event').text

