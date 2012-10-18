# -*- coding: utf-8 -*-

import webapp2
import os
import json

from picture_helper import PictureHelper

class InitStroke(webapp2.RequestHandler):
    def get(self):
        path = self.request.path
        pictures = self._get_picture(path)

        strokes = []
        for stroke in pictures.strokes:
            strokes.append(stroke)

        # strokesは単なるリストなので、cls指定は不要
        encoded = json.dumps(strokes)
        self.response.headers['Content-Type'] = 'application/json;  charset=utf-8'
        self.response.out.write(encoded)

        return



    def _get_picture(self, path):
        # /initstrokes/<id>の形式で入ってくる
        splitPath = path.split('/')

        helper = PictureHelper()
        if len(splitPath) < 3:
            # IDがない場合、指定された履歴の情報を取得する
            return helper.get_picture()

        else:
            # 指定された履歴の情報を取得する
            return helper.get_picture_by_id(splitPath[2])




debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/initstrokes', InitStroke),
                               ('/initstrokes/.*', InitStroke),
                               ], debug=debug)