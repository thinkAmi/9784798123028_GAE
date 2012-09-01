# -*- coding: utf-8 -*-

import webapp2
import datetime
import os
import logging
from google.appengine.ext import db

import gae_util
import blogs
import avatars


class ArticleTask(webapp2.RequestHandler):
    def post(self):
        
        try:
            self.update_blog(self.request)
        
        except:
            logDatetime = gae_util.Utility.convert_jst_time(datetime.datetime.utcnow())
            logging.error(logDatetime.strftime(u'%Y/%m/%d %H:%M:%S'))


    def update_blog(self, request):
    
        blog = blogs.Blog.get_by_key_name(request.get("id"))

        avatar = avatars.Avatar.get_avatar(blog.avatarId)
        avatar.create_article(blog)

        
        # 仮実装時のコード
        #utcnow = datetime.datetime.utcnow()
        #article = blogs.Article(key_name = utcnow.strftime('%Y%m%d%H%M%S'),
        #                          id = utcnow,
        #                          blog = blogEntity,
        #                          postDate = utcnow,
        #                          text = u'これはblogの本文です。',
        #                          pageUrl = u'',
        #                          imageUrl = u'http://farm2.static.flickr.com/1199/5105769215_e2110ba900_m.jpg'
        #                          )
        #
        #db.put([blogEntity, article])
        # 仮実装時のコード　ここまで
    
    
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([('/task/article', ArticleTask)], debug=debug)
