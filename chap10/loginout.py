# -*- coding: utf-8 -*-

import webapp2
import os
import re
from google.appengine.ext.webapp import template

import user_filter


GOOGLE_URL = 'https://www.google.com/accounts/o8/id'
YAHOO_URL = 'yahoo.co.jp'
HATENA_URL = 'http://www.hatena.ne.jp/＜はてなID＞'


def _encodeURIComponent(str):
    '''参考 http://d.hatena.ne.jp/ruby-U/20081110/1226313786'''
    
    def replace(match):
        return "%" + hex(ord(match.group()))[2:].upper()
    return re.sub(r"([^0-9A-Za-z!'()*\-._~])", replace, str.encode('utf-8'))

# サイトのルートパスを返す
def _create_root_path(host):
    url = host + '/index'
    return url




class Login(webapp2.RequestHandler):
    def get(self):
        # 認証サーバーからリダイレクトされるトップ画面のURLを作成する
        continuePage = _create_root_path(self.request.host_url)

        # OpenID情報をリクエスト属性に保存し、ログイン画面を表示する
        user, nickname = user_filter.do_filter()
        self.response.out.write(template.render('html/loginout.html',
                                                {
                                                 'user': user,
                                                 'nickname': nickname,
                                                 'google': self._create_login_url(continuePage, GOOGLE_URL),
                                                 'yahoo': self._create_login_url(continuePage, YAHOO_URL),
                                                 'hatena': self._create_login_url(continuePage, HATENA_URL),
                                                }))

# OpenID情報を含むURLを作成する
    def _create_login_url(self, continuePage, openidentifier):
        return '/loginhandler?continue=' + _encodeURIComponent(continuePage) + '&openid_identifier=' + _encodeURIComponent(openidentifier)



class Logout(webapp2.RequestHandler):
    def get(self):
        # 認証サーバーからリダイレクトされるトップ画面のURLを作成する
        continuePage = _create_root_path(self.request.host_url)

        # OpenID情報をリクエスト属性に保存し、ログアウト画面を表示する
        user, nickname = user_filter.do_filter()
        self.response.out.write(template.render('html/loginout.html',
                                                {
                                                 'user': user,
                                                 'nickname': nickname,
                                                 'logoutUrl': self._create_logout_url(continuePage),
                                                }))

    def _create_logout_url(self, continuePage):
        return '/logouthandler?continue=' + _encodeURIComponent(continuePage)


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/login', Login),
                               ('/_ah/login_required', Login),
                               ('/logout', Logout)
                               ], debug=debug)