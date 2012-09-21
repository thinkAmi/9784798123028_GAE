# -*- coding: utf-8 -*-

import json
import datetime
import time
from google.appengine.ext import db

import places


SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

class GaeEncode(object):

    @staticmethod
    def to_dict(models):
        dumps = []
        
        for model in models:
        
            output = {}
            
            # 削除する時のために、エンティティIDを取得しておく
            output['entityID'] = model.key().id()
            
            for key, prop in model.properties().iteritems():
                value = getattr(model, key)
                
                
                if value is None or isinstance(value, SIMPLE_TYPES):
                    output[key] = value
                    
                
                elif isinstance(value, datetime.datetime):
                    output[key] = value.strftime('%Y/%m/%d %H:%M:%S')
                    output['elapseTime'] = places.Place.get_elapse_time(value)
                    
                    
                elif isinstance(value, db.GeoPt):
                    output['lat'] = value.lat
                    output['lng'] = value.lon
                    
                    
                else:
                    raise ValueError('cannot encode' + repr(prop))

            dumps.append(json.dumps(output))



        # JSONの形に整形
        result = ','.join(dumps)
        return '[' + result + ']'
