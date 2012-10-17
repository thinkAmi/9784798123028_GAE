# -*- coding: utf-8 -*-

import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

from score import Score
from gae_util import Utility


class Ranking(webapp2.RequestHandler):
    def get(self):
        # 今月分のみ取得する検索条件を用意する
        jst = Utility.get_jst_now()
        fromRankValue = Score.get_date_offset(jst)
        toRankValue = fromRankValue + 10000


        # 今月の上位100傑を検索する
        q = db.Query(Score)
        q.filter('rankValue >=', fromRankValue)
        q.filter('rankValue <', toRankValue)
        q.order('rankValue')
        scores = q.fetch(100)

        self.response.out.write(template.render('juststop/html/ranking.html',
                                                {
                                                'rankDate': unicode(jst.year) + '/' + unicode(jst.month),
                                                'scores': scores,
                                                }))


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/juststop/ranking', Ranking),
                               ], debug=debug)