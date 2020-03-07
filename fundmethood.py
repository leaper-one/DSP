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

'''
生成一个uuid格式的trace
'''
def genTrace():
    return str(uuid.uuid1())
