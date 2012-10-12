# -*- coding: utf-8 -*-

import webapp2
import os
import random
import time
import logging

from google.appengine.ext import db
from google.appengine.ext.webapp import template

import answer

class QuizHandler(webapp2.RequestHandler):
    def get(self):
        answer = None
        pathInfo = self.request.path
        if pathInfo == None or pathInfo == '/' or pathInfo == '/index':
            # index指定の場合は、ランダムにエンティティを取得する
            answer = self.get_random_answer()

        else:
            # /index/id の場合は、特定のエンティティを取得する
            answer = self.get_answer_by_id(pathInfo)


        # 画面を表示する
        self.response.out.write(template.render('html/index.html',
                                                {
                                                 'answer': answer,
                                                }))



    def get_random_answer(self):
        # ランダムな値のすぐ次のoffset値を持つエンティティを探す
        result = self._get_entity(isFirst=True)

        if result == None:
            # エンティティが見つからない場合は、遡ってエンティティを探す
            result = self._get_entity(isFirst=False)

        if result == None:
            # 遡ってもエンティティが見つからない場合、Noneを返す
            return None

        # エンティティが見つかったら、offset値を更新して返す
        result.offset = long(time.time()) + answer.Answer.get_random_offset()
        result.put()

        return result


    def get_answer_by_id(self, entityId):
        q = db.Query(answer.Answer)
        return q.get_by_id(entityId)


    def _get_entity(self, isFirst):
        offset = long(time.time()) - answer.Answer.get_random_offset()
        logging.info(offset)

        q = db.Query(answer.Answer)
        if isFirst:
            q.filter('offset >=', offset)

        else:
            q.filter('offset <', offset)

        q.order('offset')
        return q.get()




debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/', QuizHandler),
                               ('/index', QuizHandler),
                               ('/index/*', QuizHandler),
                               ], debug=debug)