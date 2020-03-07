import os
import hashlib
import requests
import json
import time
import random
from io import BytesIO
import base64
import gzip
import uuid
import socket
from tinydb import TinyDB, Query
from secretsharing import SecretSharer, PlaintextToHexSecretSharer
import umsgpack

# from Crypto.PublicKey import RSA

# import mixin_config, assets, pressone_config

# import prs_lib
# import prs_utility

# from mixin_api import MIXIN_API

# import fundmethood as fm

# mixin_api = MIXIN_API(mixin_config)

order_db = TinyDB('order.json')
order_slice_db = TinyDB('order_slice.json')
'''
此处应当维护一张云节点 IP 列表
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
            #TO DO: 计算验证消息、打包msgpack、切片并生成列表
            order_slice_org = {
                "byte_follw": 'test'
            }#仅为测试格式
            order_slice_list = PlaintextToHexSecretSharer.split_secret(base64.b64encode(umsgpack.packb(json.dumps(order_slice_org))),2,len(DS_list))
            print(order_slice_list)
            for i in range(len(DS_list)*2):#向其他云节点广播两轮切片信息，
                for osl in order_slice_list:
                    data = {
                        "type": "order_slice",
                        "id": "uuid",
                        "data": osl
                    }
                    random_DS = random.choice(DS_list)
                    client.sendto(data, (random_DS, 8899))# 发送数据:
                    client.close()
                    