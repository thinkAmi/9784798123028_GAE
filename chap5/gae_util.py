# -*- coding: utf-8 -*-

import datetime

class Utility(object):

    @staticmethod
    def convert_jst_time(utcdatetime):
        return utcdatetime + datetime.timedelta(hours=9)
        
        
    @classmethod
    def get_jst_now(cls):
        return cls.convert_jst_time(datetime.datetime.utcnow())
