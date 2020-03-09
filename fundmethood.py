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

def slice_pack(data,min,max):#data:str,min:int,max:int
    return PlaintextToHexSecretSharer.split_secret(base64.b64encode(umsgpack.packb(data).byte),min,max)

def recover_slice(shares):#shares:List
    return SecretSharer.recover_secret(shares)

def unpackb_data(data):#data:str
    return umsgpack.unpackb(base64.b64decode(data))
