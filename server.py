import os
import hashlib
import requests
import json
import time
from io import BytesIO
import base64
import gzip
import uuid
import socket

# from Crypto.PublicKey import RSA

# import mixin_config, assets, pressone_config

# import prs_lib
# import prs_utility

# from mixin_api import MIXIN_API

# import fundmethood as fm

# mixin_api = MIXIN_API(mixin_config)


'''
此处应当维护一张云节点通讯列表
'''

DS_list = ['1','2']
global DS_list

'''
client 用于发送 UDP 消息
server 用于接收 UDP 消息
'''
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 8899)) # 绑定端口:

data = b'testaaaaaaaa'


while True:
    data, addr = server.recvfrom(1024)
    data = json.loads(data.decode('utf-8'))
    if data.get('id') != None:
        if data.get('type') == 'order':
            print('收到 '+data.get('id')+' 订单')
            # TO DO: 计算验证消息、打包msgpack、切片并生成列表
            order_slice_list = [] #生成切片信息列表
            data = None #
            a = 0
            for times in order_slice_list:
                for i in DS_list:
                    client.sendto(data[a], (i, 8899))# 发送数据:
                    client.close()
                    a += 1
        if data.get('type') == 'order_slice':
            print('收到 '+data.get('id')+' 订单切片')
            # TO Do: 收集相同 uuid 的切片，计算 BFT 结果，还原 order
