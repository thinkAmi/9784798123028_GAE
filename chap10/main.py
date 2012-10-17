# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users

import user_filter

class Main(webapp2.RequestHandler):
    def get(self):

        self.response.out.write(template.render('juststop/html/main.html',
                                                {
                                                'user': users.get_current_user()
                                                }))


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/juststop/main', Main),
                               ], debug=debug)