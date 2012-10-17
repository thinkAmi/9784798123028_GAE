# -*- coding: utf-8 -*-

import webapp2
import os
import datetime
import decimal

from google.appengine.api import users
from google.appengine.ext import db

from gae_util import Utility
from score import Score
import user_filter


class Register(webapp2.RequestHandler):
    def get(self):
        # 本とは異なり、main.htmlにuser関連の情報を持たせていないので、ここで取得する
        user, nickname = user_filter.do_filter()

        # ログインしていなければ登録しない
        if user == None:
            return


        # Over Runしていたら登録しない
        # leftLengthの算出方法は、main.jsの82行目に合わせる：小数点以下は切り捨てで計算、6での除算はトライ・アンド・エラーによるものらしい
        decimalLength = decimal.Decimal(self.request.get('leftLength'))
        leftLength = int((decimalLength / 6).to_integral_exact(rounding=decimal.ROUND_DOWN))
        if leftLength < 0:
            return


        # スコアエンティティを登録する
        accountId = user.federated_identity()
        if accountId == None:
            accountId = user.user_id()

        if nickname == None:
            nickname = 'Unknown nickname'

        jst = Utility.get_jst_now()
        offset = Score.get_date_offset(jst)
        rankValue = offset + leftLength

        q = Score(
                  key_name=accountId,
                  nickname=nickname,
                  registerDate=jst,
                  rankValue=rankValue,
                 )
        q.put()






debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/juststop/register', Register),
                               ], debug=debug)