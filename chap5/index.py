# -*- coding: utf-8 -*-

import webapp2
import os
import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import db


import blogs
import avatars
import blog_id
import gae_util


class IndexPage(webapp2.RequestHandler):
    def get(self):
        
        # ★本実装ここから
        member = avatars.Avatar.get_avatars()
        
        q = db.Query(blogs.Blog)
        q.order("-departureDate")
        results = q.fetch(10)
        # ★ここまで
        
        self.response.out.write(template.render('html/index.html',{'avatars': member,
                                                                   'blogs': results,
                                                                   }))
        
        
    def post(self):
        
        avatarClass = avatars.Avatar()
        avatar = avatarClass.get_avatar(self.request.get("avatarId"))

        jstnow = gae_util.Utility.get_jst_now()

        
        # 現在番号を取得
        blogId = blog_id.BlogId.get_by_key_name("current")
        
        if blogId is None:
            blogId = blog_id.BlogId(key_name = 'current',
                                    currentId = 0)
        
        # +1をセット
        blogId.currentId = blogId.currentId + 1
        blogId.put()
        
        id = str(blogId.currentId)
        blog = blogs.Blog(key_name = id,
                          id = blogId.currentId,
                          avatarId = avatar.id,
                          avatarName = avatar.name,
                          avatarImageName = avatar.imageName,
                          avatarMessage = avatar.message,
                          destination = self.request.get("destination"),
                          departureDate = jstnow,
                          nextPostDate = jstnow + datetime.timedelta(minutes=5),    #cronの動作間隔を指定
                          articleCount = 0)
        blog.put()
        
        
        self.response.out.write(template.render('html/index_post.html',{'blog': blog,
                                                                        }))
        
        
            
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([('/index.html', IndexPage),
                               ('/', IndexPage)], debug=debug)
