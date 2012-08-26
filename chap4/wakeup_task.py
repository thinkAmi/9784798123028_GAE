# -*- coding: utf-8 -*-

import webapp2
import logging
import datetime
import os
from google.appengine.api import mail
from google.appengine.api.labs import taskqueue

import alarm
import gae_util


# メール送信クラス
# 制御クラスからメールアドレスがひとつ送られてくるため、そのアドレスに対して送信を行う

class WakeupTask(webapp2.RequestHandler):
    def post(self):
        
        # 例外が出た場合、そのタスクは終了する(再実行させない)
        try:
            self.update_alarm(self.request)
            
        except:
            logDatetime = gae_util.Utility.convert_jst_time(datetime.datetime.utcnow())
            logging.error(logDatetime.strftime(u'%Y/%m/%d %H:%M:%S'))
            
            
    def update_alarm(self, request):
        
        email = request.get("email")
        result = alarm.Alarm.get_by_key_name(email)
        nickname = result.nickname
        count = result.count
        
        
        if count == 0:
            result.count = count + 1
            result.put()
            
            # これが実行されるとタスクも消えてしまうため、タスクを再度登録する
            taskqueue.add(url='/task/wakeuptask', params={'email': email}, countdown=300)
            
        else:
            result.delete()
        
        
        self.send_mail(email, nickname, count)
        
        
    def send_mail(self, email, nickname, count):
        
        if count == 0:
            subject = u'時間だよーー'
            body = nickname + u'頼まれていた時間だよー' + u'\n' + u'予定があるんでしょ。早く準備してね。'
        else:
            subject = u'大変ー！'
            body = nickname + u'大変大変ー！' + '\n' + u'時間過ぎているよ！' + '\n' + u'早く早く！！'
        
        mail.send_mail(sender = 'eri@thinkamigaedemo.appspotmail.com',
                       to = email,
                       subject = subject,
                       body = body)
                       
                       
                       
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
                       
app = webapp2.WSGIApplication([('/task/wakeuptask', WakeupTask)], debug=debug)
