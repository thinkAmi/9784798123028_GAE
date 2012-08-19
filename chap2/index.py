#-*- coding: utf-8 -*-

import webapp2
from google.appengine.ext.webapp import template
import logging
import os

import sentence_helper


class IndexPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render('html/index.html', {}))


    def post(self):
        result = sentence_helper.SentenceHelper.make_sentence(self.request.get('when'),
                                                              self.request.get('where'),
                                                              self.request.get('who'),
                                                              self.request.get('what'))

        self.response.out.write(template.render('html/index_post.html', {'result' : result,}))


# 環境によるデバッグフラグの設定
# See http://webapp-improved.appspot.com/guide/app.html#debug-flag
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

app = webapp2.WSGIApplication([('/', IndexPage),
                               ('/submit', IndexPage),
                               ('/index.html', IndexPage)], debug=debug)
