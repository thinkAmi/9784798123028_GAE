# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Picture(db.Model):
    # 描画した線の一覧
    # default=Noneとすることで、入力必須にはならない(空のリストが入る)
    # See: https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses?hl=ja#ListProperty
    strokes = db.ListProperty(item_type=db.Text, default=None)
    # 絵を描いているユーザーのclientIdの一覧
    clientIds = db.StringListProperty()
    # 最新の絵かどうか
    isCurrent = db.BooleanProperty()
    # 絵を描きはじめた日時
    createDate = db.DateTimeProperty(auto_now_add=True)