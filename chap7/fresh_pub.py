# -*- coding: utf-8 -*-

import json

class FreshPub(object):

    def __init__(self, title, url, salesDate):
        self.__title = title
        self.__url = url
        self.__salesDate = salesDate

    def jsonable(self):
        return dict(title=unicode(self.__title), url=self.__url, salesDate=unicode(self.__salesDate))


class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        else:
            return json.JSONEncoder.default(self, obj)
