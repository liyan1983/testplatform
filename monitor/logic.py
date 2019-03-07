#-*- coding:utf-8 -*-
# author:liyan
# datetime:2019/3/4 18:09

from mongodb.mongo import Mongo
import datetime

class Logic(object):

    def __init__(self):
        super(Logic).__init__()
        self.mongo=Mongo()

    def search(self,data):
        '''

        :param data:
        :return:
        '''
        ip=data.pop('ip','127.0.0.1')
        start=data.pop('start')
        end=data.pop('end')
        filter={
            'time':{
                '$gt': datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S"),
                '$lt': datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            }
        }
        return self.mongo.search('monitor',ip,filter)

    def get_ip_list(self):
        '''

        :return:
        '''
        return self.mongo.get_all_collections('monitor')

if __name__ == '__main__':
    logic=Logic()
    data={
        'ip':'127.0.0.1',
        'start':'2019-03-03 11:40:49',
        'end':'2019-03-03 11:41:00'
    }
    print(logic.search(data))