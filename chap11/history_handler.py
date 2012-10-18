# -*- coding: utf-8 -*-

import webapp2
import os
import json

from picture_helper import PictureHelper
from history import *

class HistoryHandler(webapp2.RequestHandler):
    def get(self):
        # 過去の絵の履歴を取得して、Historyクラスとして保存する
        histories = []

        helper = PictureHelper()
        pictures = helper.get_histories()
        for picture in pictures:
            id = picture.key().id()
            createDate = picture.createDate
            histories.append(History(id, createDate))


        # JSONで返す
        encoded = json.dumps(histories, ensure_ascii=False, cls=ComplexEncoder)
        self.response.headers['Content-Type'] = 'application/json;  charset=utf-8'
        self.response.out.write(encoded)


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/history', HistoryHandler),
                               ], debug=debug)