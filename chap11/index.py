# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.ext.webapp import template

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render('html/index.html',
                                                {
                                                }))


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/', Index),
                               ], debug=debug)