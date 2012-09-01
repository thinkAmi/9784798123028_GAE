# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.ext import db
from google.appengine.ext.webapp import template

import blogs


class BlogDisplay(webapp2.RequestHandler):
    def get(self):
        # id存在：idの記事を表示
        # id存在せず：404
        # ディレクトリ指定：最新の記事を表示
        
        blog = self.get_blog_entry(self.request.path)
        
        if blog is None:
            self.response.set_status(404)
            return self.response.out.write('404 not found')
        
        
        self.response.out.write(template.render('html/blog.html',{'blog': blog,
                                                                  # collection_nameを指定して、子クラスデータを取得
                                                                  'articles': blog.articles,
                                                                  }))


    def get_blog_entry(self, path):
        ids = path.split(u'/')
        id = ids[2]
        
        if id == '':
            return self.get_blog_entry_by_departure()
        
        return blogs.Blog.get_by_key_name(id)
        

    def get_blog_entry_by_departure(self):
        q = db.Query(blogs.Blog)
        q.order("-departureDate")
        result = q.fetch(1)
        
        # リストで返ってくることに注意
        return result[0]
        
        
    
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([('/blog/.*', BlogDisplay)], debug=debug)
