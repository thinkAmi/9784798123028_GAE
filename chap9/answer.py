# -*- coding: utf-8 -*-

import random
from google.appengine.ext import db

class Answer(db.Model):
    # 2ヶ月をミリ秒に変換したもの
    

    text = db.StringProperty()                          # 答え
    furigana = db.StringProperty()                      # ふりがな
    hints = db.StringListProperty()                     # 答えに関連するキーワード、16個入っていれば正常
    registerDate = db.DateProperty(auto_now_add=True)   # 登録日
    offset = db.IntegerProperty()                       # 登録日から計算した乱数値

    @staticmethod
    def get_random_offset():
        OFFSET_RANGE = 5184000000
        return long(random.random() * OFFSET_RANGE)
