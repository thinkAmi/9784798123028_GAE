# -*- coding: utf-8 -*-

import webapp2
import os
import json
from google.appengine.api import channel

from picture_helper import PictureHelper
from command import *

class NewPicture(webapp2.RequestHandler):
    def post(self):
        # 新しい絵を作成する。前の絵がなければ、そのまま終わる
        helper = PictureHelper()
        picture = helper.create_new_picture()
        if picture == None:
            return

        # 前の絵を描いていたクライアントに、再読み込みの指示を送信する
        clientIds = picture.clientIds
        cmd = Command('newpicture', None)
        message = json.dumps(cmd, ensure_ascii=False, cls=ComplexEncoder)

        # 接続中のクライアントに、１つずつ送信する
        for targetId in clientIds:
            channel.send_message(targetId, message)





debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/newpicture', NewPicture),
                               ], debug=debug)