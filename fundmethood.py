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
from secretsharing import SecretSharer, PlaintextToHexSecretSharer
'''
生成一个uuid格式的trace
'''
def genTrace():
    return str(uuid.uuid1())

def slice(data,min,max):
    return PlaintextToHexSecretSharer.split_secret(data,min,max)

def recover(shares):#shares:List
    return SecretSharer.recover_secret(shares)

def pack(dic):
    return base64.b64encode(umsgpack.packb(dic)).decode('UTF-8')

def unpack(pack):#data:str
    return umsgpack.unpackb(base64.b64decode(pack))

