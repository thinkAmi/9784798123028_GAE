# -*- coding: utf-8 -*-
import json

class Command(object):
    def __init__(self, name, content):
        self.__name = unicode(name)
        self.__content = unicode(content)

    def jsonable(self):
        return dict(name=self.__name, content=self.__content)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()

        else:
            return json.JSONEncoder.default(self, obj)
