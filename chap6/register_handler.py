# -*- coding: utf-8 -*-

import webapp2
import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import places
import gae_util


class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render('html/index.html',{}))
        
        
    def post(self):
        
        # 送信された情報を取得する
        nickname = self.request.get('nickname')
        tag = self.request.get('tag')
        message = self.request.get('message')
        lat = self.request.get('lat')
        lng = self.request.get('lng')
        
        
        # 入力チェック
        if nickname == '':
            self.response.out.write(template.render('html/index.html',
                                                    {
                                                     'nickname': nickname,
                                                     'tag': tag,
                                                     'message': message,
                                                     'lat': lat,
                                                     'lng': lng,
                                                     'errorNickname': True,
                                                    }))
            return
        
        
        # 位置情報をデータストアに保存する
        geo = db.GeoPt(lat, lng)
        place = places.Place(
                             nickname=nickname,
                             tag=tag,
                             message=message,
                             registDateTime=gae_util.Utility.get_jst_now(),
                             geo=geo
                             )
        place.put()
        
        
        # nicknameとtagを保存して、画面を再表示する
        self.response.out.write(template.render('html/index.html',
                                                {'nickname': nickname,
                                                 'tag': tag,
                                                }))
        
        
            
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([('/index.html', RegisterHandler),
                               ('/', RegisterHandler)
                              ], 
                              debug=debug)
