# -*- coding: utf-8 -*-

class Souvenir(object):
    
    @staticmethod
    def get_souvenir():
        return {'name': u'おみやげセット',
                'unitPrice': 1000, 
                'currency': u'JPY',
                'tax': 50, 
                'carriage': 700,
                }