# -*- coding: utf-8 -*-

import webapp2
import os
import datetime
#from google.appengine.ext.webapp import template
from google.appengine.ext import db

import gae_util
import places
import gae_encode


class PlacesJson(webapp2.RequestHandler):
    def get(self):
    
        # データストアからの抽出
        q = db.Query(places.Place)

        tag = self.request.get('tag')
        if tag != '':
            q.filter('tag =', tag)
        
        lastDateParam = self.request.get('lastDate')
        if lastDateParam != '':
            q.filter('registDateTime >', datetime.datetime.strptime(lastDateParam, '%Y-%m-%d %H:%M:%S'))

        q.order('-registDateTime')

        result = q.fetch(limit=30)



        # JSON化
        # 既存のjson.encodeではJSON化できないので、以下を参考にロジックを組む
        # http://d.hatena.ne.jp/griefworker/20100518/google_app_engine_model_json
        encoded = gae_encode.GaeEncode.to_dict(result)
        
        
        # Content-Type: text/htmlのままでも動作するものの、正しいものをセット
        self.response.headers['Content-Type'] = 'application/json;  charset=utf-8'
        
        self.response.out.write(encoded)




debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/placesjson', PlacesJson),
                              ], 
                              debug=debug)
