'''
Base on python 3.7.1 in conda.
All data pack need to follow the stander_form.md
v0.0.1:云节点异步共识核心完成
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
DS_list = ['0','1','2','3','4','5','6','7','8','9']
global DS_list

'''
client 用于发送 UDP 消息
server 用于接收 UDP 消息
'''
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 8899))

while True:
    '''
    收取 UDP 消息，变量 data 存在固定格式，具体参看 stander_form.md 
    '''
    data, addr = server.recvfrom(1024)
    data = fm.unpack(data)
    data = json.loads(data.decode('utf-8'))#data 为 dic

    if data.get('type') != None:#
        '''
        订单：接收到订单，查询是否存在于本地，若否，切片，广播分发
        '''
        if data['type'] == 'order':
            order_stored = Query()
            r = order_db.search(order_stored.order_id == data['order_id'])

            if r == []:
                #TODO: 验证订单内容
                order_slice_org = fm.genData('order',data['user_id'],data['data'],order_id=data['order_id'])
                order_db.insert(order_slice_org)#储存订单
                order_slice_list = fm.slice(order_slice_org,len(DS_list)*2//3+1,len(DS_list))#打包msgpack
                
                for i in range(len(DS_list)*2):#向其他云节点广播两轮 order_slice 信息
                    for osl in order_slice_list:
                        data = fm.genData("order_slice",user_id=order_slice_org["user_id"],order_id=order_slice_org["order_id"],data=[osl])
                        data = fm.pack(data)
                        client.sendto(data, (random.choice(DS_list),8899))# 广播数据
        '''
        订单切片
        '''
        if data.get('type') == 'order_slice':
            Slice = Query()#查询相同 order_id 的切片文件
            r = order_slice_db.search(Slice.data['order_id'])
            if r == []:
                order_slice_db.insert(data)
                for i in range(len(DS_list)//2):
                    client.sendto(fm.pack(data),(random.choice(DS_list), 8899))#再广播:
                    client.close()
            else:
                order_slice_db.insert(data)
                Slice = Query()#查询相同 order_id 的切片文件
                r = order_slice_db.search(Slice.data['order_id'])
                data = fm.genData('order_slice',user_id=data['user_id'],data=r)
                client.sendto(fm.pack(data), (random.choice(DS_list), 8899))#再广播:
                client.close()
            a = list(set(order_slice_db.search(Slice.order_id)))#去重
            if len(a) > len(DS_list)*2//3+1:#判断 BFT 结果，并还原
                a = fm.recover(a)
                print(a)
                #TODO:根据还原结果，进行处理
                