# -*- coding: utf-8 -*-

import webapp2
import datetime
import os
from google.appengine.api.labs import taskqueue

import alarm
import gae_util

        
class Wakeup(webapp2.RequestHandler):
    def get(self):
        results = alarm.Alarm.all()
        jstNow = gae_util.Utility.convert_jst_time(datetime.datetime.utcnow())
        
        results.filter("wakeupDate <= ", jstNow).order("wakeupDate")
        

        
        # 登録件数は多くない前提のため、イテレータにて全数取得する
        for result in results:
            taskqueue.add(url='/task/wakeuptask', params={'email': result.email})
            
            
            
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

app = webapp2.WSGIApplication([('/cron/wakeup', Wakeup)], debug=debug)
