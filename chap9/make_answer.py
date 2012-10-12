# -*- coding: utf-8 -*-

import webapp2
import os
import logging

from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

import answer
from goo.goo_helper import GooHelper

class MakeAnswerHandler(webapp2.RequestHandler):
    def get(self):
        try:
            # gooキーワードランキングの結果を答えとして登録する
            words = GooHelper.get_words()
            for text in words:
               taskqueue.add(url='/task/makeanswer', params={'text': text}, countdown=300)
        except Exception, e:
            logging.warning(e)


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/cron/makeanswer', MakeAnswerHandler),
                               ], debug=debug)