# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.api import channel

from picture_helper import PictureHelper

class TokenHandler(webapp2.RequestHandler):
    def get(self):
        # クライアントIDを取得する
        clientId = self.request.get("clientId")
        helper = PictureHelper()
        helper.connect_picture(clientId)

        # トークンを生成する
        token = channel.create_channel(clientId)

        # JSONの形にして返す
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(token)


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/gettoken', TokenHandler),
                               ], debug=debug)