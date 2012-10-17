# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        # 入力されたOpenID情報を取得する
        continuePage = self.request.get('continue')
        openidIdentifier = self.request.get('openid_identifier')

        # OpenIDの認証サーバー情報を取得する
        # See https://developers.google.com/appengine/docs/python/users/functions?hl=ja
        url = users.create_login_url(
                                     dest_url=continuePage,        # リダイレクトURL
                                     federated_identity=openidIdentifier,     # 入力されたOpenID
                                    )
        self.redirect(url)


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        # 入力されたログオフ後のリダイレクト情報を取得する
        continuePage = self.request.get('continue')

        url = users.create_logout_url(dest_url=continuePage)
        self.redirect(url)


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/loginhandler', LoginHandler),
                               ('/logouthandler', LogoutHandler),
                               ], debug=debug)