# -*- coding: utf-8 -*-

import webapp2
import os
import json
from google.appengine.api import channel

from picture_helper import PictureHelper
from command import *

class AddStroke(webapp2.RequestHandler):
    def post(self):
        
        clientId = self.request.get('clientId')
        stroke = self.request.get('stroke')

        # 描画情報を登録する
        helper = PictureHelper()
        picture = helper.add_stroke(stroke)


        # 描画情報をチャネルサービスに送信する
        clientIds = picture.clientIds
        cmd = Command('addstroke', stroke)
        message = json.dumps(cmd, ensure_ascii=False, cls=ComplexEncoder)


        # 接続中のクライアントに、１つずつ送信する
        for targetId in clientIds:
            # 自分自身は除く
            if targetId == clientId:
                continue

            channel.send_message(targetId, message)





debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/addstroke', AddStroke),
                               ], debug=debug)