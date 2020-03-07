import os
import hashlib
import mixin_config
import uuid
from mixin_api import MIXIN_API
from mixin_ws_api import MIXIN_WS_API
# import prs_utility
from flask import Flask, render_template, g, request, redirect, session, url_for, flash, Blueprint
from flask_restful import Api, Resource
from Crypto.PublicKey import RSA

import requests
import json
import time
from io import BytesIO
import base64
import gzip
# import prs_lib
import pressone_config
from assets import CNB


mixin_api = MIXIN_API(mixin_config)
mixinApiBotInstance = MIXIN_API(mixin_config)

# client = prs_lib.PRS({
#   'env': 'dev',
#   'private_key': '01e05107e3141083f66aa2ec5fa78d095115a912ca17148813b87d4313115837',
#   'address': 'acd8960a52de7017059cfd6c7113f073fad2a2a2e',
#   'debug': True,
# })

'''
生成公钥
'''
def pubkeyContent(inputContent):
    contentWithoutHeader= inputContent[len("-----BEGIN PUBLIC KEY-----") + 1:]
    contentWithoutTail = contentWithoutHeader[:-1 * (len("-----END PUBLIC KEY-----") + 1)]
    contentWithoutReturn = contentWithoutTail[:64] + contentWithoutTail[65:129] + contentWithoutTail[130:194] + contentWithoutTail[195:]
    return contentWithoutReturn
'''
生成api实例
'''
def generateMixinAPI(private_key,pin_token,session_id,user_id,pin,client_secret):
    mixin_config.private_key       = private_key
    mixin_config.pin_token         = pin_token
    mixin_config.pay_session_id    = session_id
    mixin_config.client_id         = user_id
    mixin_config.client_secret     = client_secret
    mixin_config.pay_pin           = pin
    return  MIXIN_API(mixin_config)
'''
生成一个uuid格式的trace
'''
def genTrace():
    return str(uuid.uuid1())

'''
生成一个bot收款链接，需传入trace
'''
def genAPaylink(trace=genTrace(), asset=CNB, amount='1', memo='1'):
    return "https://mixin.one/pay?recipient="+mixin_config.client_id+"&asset="+asset+"&amount="+amount+"&trace="+trace+"&memo="+memo



'''
对一个文本签名
'''
def sign_text(userid, signer2, data):
    texthash = prs_utility.keccak256(text=userid+r'\n'+signer2+r'\n'+data)

    data = {
        'file_hash': texthash,
    }

    sig = prs_utility.sign_block_data(data, private_key=pressone_config.private_key)
    post_url = 'https://press.one/api/v2/datasign'

    payload = {
        'user_address': pressone_config.address,
        'type': 'PUBLISH:2',
        'meta': {
            'uris': '',
            'mime': 'text/markdown;UTF-8'
        },
        'data': data,
        'hash': prs_utility.hash_block_data(data),
        'signature': sig.get('signature')
    }

    req = requests.post(post_url, json=payload)

    return req.json()


def pub_text(userid, data, trace=genTrace()):
    texthash = prs_utility.keccak256(text=userid+r'\n'+data+r'\n'+trace)

    data = {
        'file_hash': texthash,
    }

    sig = prs_utility.sign_block_data(data, private_key=pressone_config.private_key)
    post_url = 'https://press.one/api/v2/datasign'

    payload = {
        'user_address': pressone_config.address,
        'type': 'PUBLISH:2',
        'meta': {
            'uris': '',
            'mime': 'text/markdown;UTF-8'
        },
        'data': data,
        'hash': prs_utility.hash_block_data(data),
        'signature': sig.get('signature')
    }

    req = requests.post(post_url, json=payload)

    return req.json()



def genMixinUser():
    key = RSA.generate(1024)
    pubkey = key.publickey()
    # print(key.exportKey())
    # print(pubkey.exportKey())
    private_key = key.exportKey()
    session_key = pubkeyContent(pubkey.exportKey())
    # print(session_key)
    # print(session_key.decode())
    userInfo = mixinApiBotInstance.createUser(session_key.decode(),"Tom Bot")
    print(userInfo.get("data").get("user_id"))
    # print([private_key.decode(),
    #                     userInfo.get("data").get("pin_token"),
    #                     userInfo.get("data").get("session_id"),
    #                     userInfo.get("data").get("user_id"),
    #                     PIN])
    mixinApiNewUserInstance = generateMixinAPI(private_key.decode(),
                                                userInfo.get("data").get("pin_token"),
                                                userInfo.get("data").get("session_id"),
                                                userInfo.get("data").get("user_id"),
                                                "","")
    # pinInfo = mixinApiNewUserInstance.updatePin(PIN,"")
    # print(pinInfo)
    # time.sleep(3)
    # # mixinApiNewUserInstance.pay_pin = PIN
    # pinInfo2 = mixinApiNewUserInstance.verifyPin(PIN2)
    # print(pinInfo2)

    return mixinApiNewUserInstance
    