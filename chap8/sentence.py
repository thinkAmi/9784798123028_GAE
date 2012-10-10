# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Sentence(db.Model):
    # 主キーはツイートのID
    # 投稿者の名前
    screenName = db.StringProperty()
    # 元のツイート文章
    text = db.StringProperty()
    # 名詞を抜いた文章
    chippedText = db.StringProperty()
    # 抜いた名詞の品詞
    chips = db.StringListProperty()
    # 単語を抽出するためのランダムな値
    rand = db.FloatProperty()
    # 作成日時：UTCタイムゾーン
    registerUtcDate = db.DateProperty(auto_now_add=True)