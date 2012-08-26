# -*- coding: utf-8 -*-

import webapp2
import os
import email
from google.appengine.api import mail

import alarm


class Receive(webapp2.RequestHandler):
    def post(self):
        message = mail.InboundEmailMessage(self.request.body)
        
        #emailモジュールにて、名前とメールアドレスを分離
        address = email.utils.parseaddr(message.sender)
        result = alarm.Alarm.get_by_key_name(address[1])
        result.delete()
        
        
        
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

#以下の「<your application mail>」は、自分のアプリケーション用のメールアドレスに差し替える
app = webapp2.WSGIApplication([('/_ah/mail/<your application mail>', Receive)], debug=debug)
