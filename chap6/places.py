# -*- coding: utf-8 -*-

import datetime
from google.appengine.ext import db

import gae_util

class Place(db.Model):
    nickname = db.StringProperty()
    tag = db.StringProperty()
    message = db.StringProperty()
    registDateTime = db.DateTimeProperty()
    geo = db.GeoPtProperty()
    
    
    @staticmethod
    def get_elapse_time(regist):

        # 内部では、days,seconds,microsecondsしか持っていないことに注意
        delta = (gae_util.Utility.get_jst_now() - regist)
        
        # 10日以上昔
        if (delta > datetime.timedelta(days=10)):
            return u'だいぶ前'
            
            
        # 日
        elif (delta > datetime.timedelta(days=1)):
            return str(delta.days) + u'日前'
        
        # 時間
        elif (delta > datetime.timedelta(hours=1)):
            return str(delta.seconds / 3600) + u'時間前'
            
        # 分
        elif (delta > datetime.timedelta(minutes=1)):
            return str(delta.seconds / 60) + u'分前'
            
            
        # 秒
        elif (delta > datetime.timedelta(seconds=1)):
            return str(delta.seconds) + u'秒前'
            
            
        # 秒未満
        else:
            return u'1秒未満'
