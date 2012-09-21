# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.ext.webapp import template


class MapHandler(webapp2.RequestHandler):
    def get(self):
        tag = self.request.get('tag')
        
        self.response.out.write(template.render('html/map.html',
                                                {
                                                 'tag': tag,
                                                }))
    
    
    
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([('/map', MapHandler),
                              ], 
                              debug=debug)
