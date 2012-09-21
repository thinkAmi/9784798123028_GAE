# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.ext import db

import places


class DeletionHandler(webapp2.RequestHandler):
    def get(self):
        data = places.Place.get_by_id(long(self.request.get('entityID')))
        data.delete()
    

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/delete', DeletionHandler),
                              ], 
                              debug=debug)
