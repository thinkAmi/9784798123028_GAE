# -*- coding: utf-8 -*-

import webapp2
import datetime
import os
from google.appengine.api.labs import taskqueue

import blogs
import gae_util

import logging

        
class ArticleOperation(webapp2.RequestHandler):
    def get(self):
        results = blogs.Blog.all()
        jstNow = gae_util.Utility.convert_jst_time(datetime.datetime.utcnow())
        
        results.filter("nextPostDate <= ", jstNow).order("nextPostDate")
        
        for result in results:
            taskqueue.add(url='/task/article', params={'id': result.id})
            
            
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

app = webapp2.WSGIApplication([('/cron/article', ArticleOperation)], debug=debug)
