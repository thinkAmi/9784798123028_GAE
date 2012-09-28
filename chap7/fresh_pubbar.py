# -*- coding: utf-8 -*-

import webapp2
import os
import logging
import json

import amazon.amazon_helper
import fresh_pub


class FreshPubbar(webapp2.RequestHandler):
    def get(self):
        
        # レスポンスの形式を、JSONに変更する
        self.response.headers['Content-Type'] = 'application/json;  charset=utf-8'
        
        
        # 新刊情報を取得する
        title = self.request.get('title')
        author = self.request.get('author')
        publisher = self.request.get('publisher')
        if title == '' and author == '' and publisher == '':
            # 条件が指定されていなければ、Pythonの本を検索する
            title = 'Python'

        helper = amazon.amazon_helper.AmazonHelper()
        results = helper.get_fresh_pubs(title, author, publisher)
        

        # 新刊情報をJSONで返す
        encoded = json.dumps(results, ensure_ascii=False, cls=fresh_pub.ComplexEncoder)
        self.response.out.write(encoded)



debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/freshpubbar', FreshPubbar),
                              ], debug=debug)
