# -*- coding: utf-8 -*-

import webapp2
import os
import re
import random

from twitter.twitter_helper import TwitterHelper as Twitter
from yahoo.yahoo_helper import YahooHelper as Yahoo

import api_config
import sentence
import word


URL_PATTERN = r'[\w]\.\-/:#\?=&;%~\+]+'
UNOFFICIAL_RETWEET_PATTERN = r'(^|\s)[RQ]\s'


class GatherHandler(webapp2.RequestHandler):
    def get(self):

        # ぐぐるちゃんのユーザーを取得しておく
        guguruchan = Twitter.get_guguruchan()

        # フォロワーのツイート一覧を取得する
        timeline = Twitter.get_follower_timeline()

        # ツイートを１つずつ解析して、データストアに保存する
        for status in timeline:
            # 自分自身のツイートは解析しない
            if guguruchan.GetId() == status.GetUser().GetId():
                continue

            self.analyze_status(status)



    # ツイートを解析する
    def analyze_status(self, status):
        # http/httpsで始まるURLは、無意味な文字列なので除去する
        text = re.sub(URL_PATTERN, '', status.GetText())

        # 登録しないツイート
        # api.GetUserTimeline()にて、公式RTは取得しないようにしているため、その分のチェックは不要
        if re.match('@', text):     # リプライ
            return

        # 非公式RT/QT
        if re.search(UNOFFICIAL_RETWEET_PATTERN, text):
            return


        # ツイートのテキストを解析する
        helper = Yahoo(api_config.Yahoo.APPLICATION_ID)
        chips = []
        chipTexts = []
        for chunk in helper.get_chunk_list(text):
            chip, chipText = self.analyze_feature(chunk, len(chips))

            if chip:
                chips.append(chip)

            chipTexts.append(chipText)

        # 登録しないツイート (その2)
        if len(chips) == 0:         # 名詞のないもの
            return


        # 文書データクラスを保存する
        q = sentence.Sentence(
                              key_name=unicode(status.GetId()),
                              screenName=status.GetUser().GetScreenName(),
                              text=text,
                              chippedText=''.join(chipTexts),
                              chips=chips,
                              rand=random.random()
                              )
        q.put()



    # 品詞を解析する
    def analyze_feature(self, chunk, chipsSize):
        # 特殊な品詞は除外する
        if chunk.length < 4:
            return

        # 品詞が名詞ならば、置換え用の場所を用意して、単語をデータストアに保存する
        if chunk.pos == u'名詞':
            q = word.Word(
                          key_name=chunk.surface,
                          posDetail=chunk.posDetail,
                          rand = random.random()
                          )
            # キーが同じ場合上書きされてしまうが、今回の場合は特に問題ない
            q.put()

            chipText = '{' + unicode(chipsSize) + '}'
            return chunk.posDetail, chipText


        # 名詞以外であれば、単語をそのまま使う
        else:
            return None , chunk.surface


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/cron/gather', GatherHandler),
                               ], debug=debug)