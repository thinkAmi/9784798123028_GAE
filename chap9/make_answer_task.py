# -*- coding: utf-8 -*-

import webapp2
import os
import time
import logging

from google.appengine.ext import db

import answer
from yahoo.yahoo_helper import YahooHelper

class MakeAnswerTaskHandler(webapp2.RequestHandler):
    def post(self):
        try:
            text = self.request.get('text')
            self._register(text)
        except Exception, e:
            logging.warning(e)


    # Answerエンティティの登録
    def _register(self, text):
        helper = YahooHelper()
        # ヒントの数が16個に足りないものは、登録しない
        hints = helper.get_hints(text)

        if len(hints) < 16:
            return

        # これ以降はデータストアの登録/更新が確定しているため、offset値を取得しておく
        offset = long(time.time()) + answer.Answer.get_random_offset()
        logging.info('convert-long')

        # 答え(text)にユニークキー制約をもたせられないので、そのプロパティが存在するかチェックし、put()
        q = db.Query(answer.Answer)
        q.filter('text =', text)
        result = q.get()

        if result:
            # すでに登録されている答えは、最新のヒントで上書きする
            result.hints = hints
            result.offset = offset
            result.put()

        else:
            # 新規の答えを追加する
            furigana = helper.get_furigana(text)

            a = answer.Answer(
                              text=text,
                              furigana=furigana,
                              hints = hints,
                              offset=offset
                              )
            a.put()





debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/task/makeanswer', MakeAnswerTaskHandler),
                               ], debug=debug)


