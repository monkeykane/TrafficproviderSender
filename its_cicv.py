#!/usr/bin/env python
#coding=utf8

import time
import json
import socket
import urllib
import urllib.request
import random
import math
from GeographicFrame import GeographicFrameEnu
from GIS import GIS

ORILAT=31.2828880548475
ORILON=121.171131134033
ORIALT=0
pulse = 0.1
tick = 0

lastData = [{"vid":3,"laneid":"123","coordinate":{"x":121.173791995,"y":31.2836465696,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":304.94431978549636,"speed":15.036970176916503,"vcolor":"ffff00","timestamp":1584541180997}]

def parseData(src_data, frameEnu, socket):
        #json_str = src_data
        #json_str = json.dumps(src_data)
        # print(json_str)
        # print(type(json_str))
        # 将JSON数据解码为dict（字典）
        
        #datas = json.loads(json_str)
        for singleData in src_data:
            # print ('---------')
            # print ('x:' + str(singleData['coordinate']['x']))
            # print ('y:' + str(singleData['coordinate']['y']))
            # print ('z:' + str(singleData['coordinate']['z']))
            # print (singleData)


            out = frameEnu.WgsToLocal(float(singleData['coordinate']['y']), float(singleData['coordinate']['x']), float(singleData['coordinate']['z']))
            # print(out.x, out.y)
        
            actor = {}
            global tick
            actor["Time"] = str(tick) #str(singleData['timestamp'])
            actor["Speed"] = str(singleData['speed'])
            actor["ID"] = str(singleData['vid'])
            assetID = 1000000 + singleData['vid']
            if assetID > 1000058:
                assetID = random.randint(1000000,1000058)
            actor["AssetID"] = str(assetID) #str(random.randint(1000000,1000058))
            actor["Rotation"] = str(GIS.DegreeToRadian(90.000-singleData['courseAngle']))
            actor["PositionZ"] = str(singleData['coordinate']['z']+0.9)
            actor["PositionX"] = str(out.x)
            actor["PositionY"] = str(out.y)
            #print('ready to send:' + str(actor))
            try:
                socket.send((json.dumps(actor) + '@').encode('utf-8'))                
            except:
                print('traffic provider is closed: ' + str(singleData['timestamp']))



if __name__ == '__main__':
    frameEnu = GeographicFrameEnu(ORILAT,ORILON,ORIALT)
    trafficProviderSocket = socket.socket()
    trafficProviderSocket.connect(("127.0.0.1", 21568))
    print("start data process node...\n")
    print("connect traffic provider ip: 127.0.0.1 port:21568")

    while (True):
        start = time.time()
        tick = start
        try:
            url = "http://120.133.21.14:8090/gqApp/monitor/regionCloud/map?v2xId=210"
            data = urllib.request.urlopen(url, timeout=0.08).read()
            data_response = json.loads(data) #data.decode('UTF-8')
#            print(data_response)
            if (len(data_response) == 0):
#                print('get src data empty!')
                time.sleep(0.001)
                continue
            lastData = data_response
            # print("---------------" + str(data_response))
        except Exception as e:
            print("+++++++++++++++" +str(e))
        
        parseData(lastData, frameEnu, trafficProviderSocket)    
        
        end = time.time()
        if ( pulse > (end-start)):
            time.sleep(pulse - (end-start)) 