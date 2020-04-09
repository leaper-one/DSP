import os
import hashlib
import uuid
from Crypto.PublicKey import RSA
import requests
import json
import time
from io import BytesIO
import base64
import gzip
import pressone_config
from assets import CNB
import umsgpack
from inspect import signature
from secretsharing import SecretSharer, PlaintextToHexSecretSharer
'''
生成一个uuid格式的trace
'''
def genTrace():
    return str(uuid.uuid1())
'''
切片四件套
使用：
1.将需要的字符串 data 进行 slice 得到多分切片，
2.将每份切片 进行 pack 用以传输，
3.将单份进行 unpack 得到切片，
4.将多分切片进行 recover 还原 data。
'''
def slice(data,min,max):
    return PlaintextToHexSecretSharer.split_secret(data,min,max)

def recover(shares):#shares:List
    return SecretSharer.recover_secret(shares)

def pack(dic):
    return base64.b64encode(umsgpack.packb(dic)).decode('UTF-8')

def unpack(pack):#data:str
    return umsgpack.unpackb(base64.b64decode(pack))

def genData(type,user_id=None,data=None,order_id=None):
    if type == 'order':
        r = {
            "type": "order",
            "user_id": user_id,
            "order_id": order_id,
            "data": data,
        }
    elif type == 'order_slice':
        r = {
            "type": "order_slice",
            "user_id": user_id,
            "order_id": order_id,
            "data": data
        } 
    
    return r
