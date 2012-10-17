# -*- coding: utf-8 -*-

from google.appengine.ext import db

from gae_util import Utility

class Score(db.Model):
    #主キー：AccounID
    # 登録した人の名前
    nickname = db.StringProperty()
    # 登録日時(JSTで登録するため、自動で登録するauto_nowは使えない)
    registerDate = db.DateTimeProperty()
    # 登録月 + 残り距離
    # Pythonの場合、longはメモリが許す限りの範囲を扱えるため、IntegerPropertyを使う
    rankValue = db.IntegerProperty()

    # 登録データから残り距離を計算して返すヘルパーメソッド
    # htmlテンプレートの中で使用する
    def get_left_length(self):
        jst = Utility.convert_jst_time(self.registerDate)
        offset = self.get_date_offset(jst)

        return unicode(float(self.rankValue - offset) / 10)


    @staticmethod
    def get_date_offset(jst):
        year = jst.year
        month = jst.month
        monthOffset = 10 if month < 10 else 1

        return year * 1000000 + month * 10000 * monthOffset



