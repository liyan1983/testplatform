#coding=utf-8

import time
import socket
import datetime

import psutil

from infrastructure import send_email
from infrastructure.mongo import Mongo


class Agent(object):

    def __init__(self):
        super(Agent).__init__()
        self.mongo = Mongo()

    def get_ip(self):
        """
        通过socket库可以获取机器名，通过机器名可以获取ip地址。
        :return:
        """
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        # return ip
        return '127.0.0.1'

    def get_cpu(self):
        """
        interval代表我们获取cpu数据的时间间隔，percpu为True时，如果机器多核，则返回多个核数据。
        :return:
        """
        result = {}
        data = psutil.cpu_percent(interval=1, percpu=True)
        result['avg'] = sum(data) / psutil.cpu_count()
        result['idle'] = 100 - result['avg']
        result['data'] = data
        return result

    def get_memory(self):
        result = {}
        data = psutil.virtual_memory()
        # 内存总量
        result['total'] = data.total
        # 可用内存
        result['available'] = data.available
        # 已用内存占比
        result['percent'] = data.percent
        # 已使用内存
        result['used'] = data.used
        return result

    def get_disk(self):
        result = {
            'total': 0,
            'used': 0,
            'free': 0,
            'percent': 0
        }
        # 先获取硬盘分区，再跟进分区获取硬盘信息，Mac这里直接用/代替disk_partitions()
        partitions = psutil.disk_partitions()
        # 计算每一个分区的数据，然后汇总成硬盘使用总量
        for partition in partitions:
            data = psutil.disk_usage(partition.device)
            result['total'] += data.total
            result['used'] += data.used
            result['free'] += data.free
        result['percent'] = 100 * result['used'] / result['total']
        return result

    def get_network(self):
        """
        获取网卡接受与发送的bytes和packet数据。
        :return:
        """
        result = {
            'bytes': {},
            'packets': {}
        }
        data = psutil.net_io_counters()
        result['bytes']['sent'] = data.bytes_sent
        result['bytes']['receive'] = data.bytes_recv
        result['packets']['sent'] = data.packets_sent
        result['packets']['receive'] = data.packets_recv
        return result

    def monitor(self, interval):
        """
        :param interval:
        :return:
        """
        collection = self.get_ip()
        while True:
            result = {
                'time': datetime.datetime.now(),
                'cpu': self.get_cpu(),
                'memory': self.get_memory(),
                'disk': self.get_disk(),
                'network': self.get_network(),
            }
            if result['cpu']['avg'] > 20:
                send_email("429245203@qq.com", "<h1>CPU使用率大于20%，实际是{0}</h1>".format(result['cpu']['avg']))
            print("将机器{0}数据写入数据库{1}".format(collection, result))
            self.mongo.insert("monitor", collection, result)
            time.sleep(interval)


if __name__ == '__main__':
    agent = Agent()
    agent.monitor(1)
