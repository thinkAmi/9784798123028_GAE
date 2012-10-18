# -*- coding: utf-8 -*-
import json
import datetime
import time

from gae_util import Utility

class History(object):
    def __init__(self, id, createDate):
        self.__id = unicode(id)

        jst = Utility.convert_jst_time(createDate)
        # self.__createDate = jst.strftime('%Y年%m月%d日 %H時%M分ごろの絵') とやりたいけれど、unicodeを渡せない
        # 改行して見やすくするために、右辺はカッコで閉じている
        self.__createDate = ( unicode(jst.year) + u'年'
                            + unicode(jst.month) + u'月'
                            + unicode(jst.day) + u'日　'
                            + unicode(jst.hour) + u'時'
                            + unicode(jst.minute) + u'分ごろの絵' )

    def jsonable(self):
        return dict(id=self.__id, createDate=self.__createDate)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()

        else:
            return json.JSONEncoder.default(self, obj)
