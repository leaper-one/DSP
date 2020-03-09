'''
Base on python 3.7.1 in conda.
All data pack need to follow the stander_form.md
'''
import os
import hashlib
import requests
import json
import time
import random
import base64
import gzip
import uuid
import socket
import umsgpack
from io import BytesIO
from tinydb import TinyDB, Query
from secretsharing import SecretSharer, PlaintextToHexSecretSharer
import fundmethood as fm
# from Crypto.PublicKey import RSA

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

while True:
    data, addr = server.recvfrom(1024)
    data = json.loads(data.decode('utf-8'))
    if data.get('type') != None:
        if data.get('type') == 'order':
            order_stored = Query()
            r = order_db.search(order_stored.order_id == data['order_id'])
            if r == []:
                print('收到 '+data.get('id')+' 订单')
                #TODO: 计算验证消息、储存订单、打包msgpack、切片并生成列表
                order_slice_org = {
                    "type": "order",
                    "user_id": data['user_id'],
                    "order_id": data['order_id'],
                    "data": {#TODO:需更改
                        "file_type": "mine",
                        "file_hash": "str(md5)",
                        "file_slices_hash": "list"
                    },
                    "date":"str",
                    "order_hash":"str"
                }#仅为测试格式,需要转换成 stander_form.md 中的标准格式
                order_db.insert(order_slice_org)
                order_slice_list = fm.slice_pack(order_slice_org,len(DS_list)*(2/3)+1,len(DS_list))
                print(order_slice_list)
                for i in range(len(DS_list)*2):#向其他云节点广播两轮切片信息
                    for osl in order_slice_list:
                        data = {
                            "type": "order_slice",
                            "user_id":order_slice_org["user_id"],
                            "order_id": order_slice_org["order_id"],
                            "order_hash":order_slice_org["order_hash"],
                            "data": osl
                        }
                        random_DS = random.choice(DS_list)
                        client.sendto(data, (random_DS, 8899))# 广播数据:
                        client.close()
            else:
                pass
                    
        if data.get('type') == 'order_slice':
            print('收到 '+data.get('id')+' 订单切片')
            #TODO: 收集相同 uuid 的切片，计算 BFT 结果，储存或抛弃、还原 order
            #TODO: 查找数据库中相同的订单号的切片文件
            Slice = Query()
            r = order_slice_db.search(Slice.id)
            if r == []:
                order_slice_db.insert(data)
            else:
                if 
            data.get('order_id')
            #TODO: 求公共子集
            #TODO: 判断 BFT 结果
            #TODO: 将以上整理为一个判断流程
            
            if len() >= 7*(2/3)+1:
                pass
            