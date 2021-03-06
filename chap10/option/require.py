# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.ext.webapp import template

import user_filter

class Require(webapp2.RequestHandler):
    def get(self):
        user, nickname = user_filter.do_filter()

        self.response.out.write(template.render('html/require.html',
                                                {
                                                'user': user,
                                                'nickname': nickname,
                                                }))


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/require', Require),
                               ], debug=debug)