# -*- coding: utf-8 -*-

import webapp2
import os
import random
import copy
import datetime

from google.appengine.ext import db

from twitter.twitter_helper import TwitterHelper
import sentence
import word



class TweetHandler(webapp2.RequestHandler):
    def get(self):
        # 文章を取得する
        s = self.get_random_entity(db.Query(sentence.Sentence), None)
        if s == None:
            return

        # 置換する単語を取得する
        chipCount = len(s.chips)

        arguments = []
        for i in range(chipCount):
            chip = s.chips[i]
            w = self.get_random_entity(db.Query(word.Word), chip)
            arguments.append(u'ぬる' if w == None else w.key().name())

        # 文章の名詞の入る場所に名詞を当て込む
        chippedText = s.chippedText
        text = chippedText.format(*arguments)

        # ツイートを投稿する
        TwitterHelper.tweet(unicode(text))



    def get_random_entity(self, entity, posDetail):
        # ランダムな値のすぐ次のrand値を持つエンティティを探す
        result = self._get_entity(entity, posDetail, True)

        # ランダムな値のすぐ次のエンティティが見つからない場合は、先頭のエンティティを探す
        if result == None:
            result = self._get_entity(entity, posDetail, False)

        # エンティティが見つかったら、rand値を更新して返す
        if result != None:
            result.rand = random.random()
            result.put()

            return result

        # エンティティが見つからなかったら、Noneを返す
        return None


    def _get_entity(self, entity, posDetail, isRandom):
        # entityは再利用するため、deepコピーしておく
        q = copy.deepcopy(entity)

        if isRandom:
            q.filter('rand >=', random.random())

        if posDetail:
            q.filter('posDetail =', posDetail)

        q.order('rand')
        return q.get()


class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        # 削除するデータの日付
        utcToday = datetime.datetime.utcnow().date()
        # およそ90日が有効期限
        expireDate = utcToday - datetime.timedelta(days=90)

        # 古い文章データクラスの取得
        q = db.Query(sentence.Sentence)
        q.order('id')
        results = q.fetch(100)

        # 文章データクラスの削除
        for result in results:
            registerDate = result.registerUtcDate

            if registerDate != None and registerDate > expireDate:
                # 有効期限より新しい文章データクラスが出てきたら、削除処理を終了
                return

            db.delete(result)




class RefollowHandler(webapp2.RequestHandler):
    def get(self):
        # フォロー返しをする
        TwitterHelper.refollow();

class RemoveHandler(webapp2.RequestHandler):
    def get(self):
        # リムーブする
        TwitterHelper.remove()



debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([
                               ('/cron/tweet', TweetHandler),
                               ('/cron/delete', DeleteHandler),
                               ('/cron/refollow', RefollowHandler),
                               ('/cron/unfollow', RemoveHandler),
                               ], debug=debug)