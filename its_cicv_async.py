import aiohttp, asyncio
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


 
async def main():#aiohttp必须放在异步函数中使用
    frameEnu = GeographicFrameEnu(ORILAT,ORILON,ORIALT)
    trafficProviderSocket = socket.socket()
    trafficProviderSocket.connect(("127.0.0.1", 21568))
    print("start data process node...\n")
    print("connect traffic provider ip: 127.0.0.1 port:21568")

    while (True):   
        start = time.time()  
        tasks = []
        tasks.append(fetch('http://120.133.21.14:8090/gqApp/monitor/regionCloud/map?v2xId=210', frameEnu, trafficProviderSocket))
    #    [tasks.append(fetch('https://api.github.com/events?a={}'.format(i))) for i in range(10)]#十次请求
        await asyncio.wait(tasks)
        end = time.time()
        # if ( pulse > (end-start)):
        #     time.sleep(pulse - (end-start)) 
        global tick
        tick = tick + pulse
 
async def fetch(url, frameEnu, socket):
    async with aiohttp.request('GET', url) as resp:
        jsonresp = await resp.json()
        # print(jsonresp) 

        src_data = jsonresp

        if (len(jsonresp) == 0): # using fake data to simulate
            src_data = [{"vid":31,"laneid":"123","coordinate":{"x":121.174872196,"y":31.2828974608,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":321.2275983709814,"speed":15.935495485772357,"vcolor":"ffff00","timestamp":1584351080687},{"vid":32,"laneid":"123","coordinate":{"x":121.166487212,"y":31.2827394416,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":80.29714276714778,"speed":7.595814958732172,"vcolor":"ffff00","timestamp":1584351099409},{"vid":33,"laneid":"123","coordinate":{"x":121.174882629,"y":31.2828868575,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":321.6544039738544,"speed":16.1701961617145,"vcolor":"ffff00","timestamp":1584351085214}]            
            print('Fake data!')
            # time.sleep(0.001) 
            # return        

        json_str=json.dumps(src_data)
        # print(json_str)
        # print(type(json_str))
        # 将JSON数据解码为dict（字典）
        
        datas = json.loads(json_str)
        for singleData in datas:
            # print ('---------')
            # print ('x:' + str(singleData['coordinate']['x']))
            # print ('y:' + str(singleData['coordinate']['y']))
            # print ('z:' + str(singleData['coordinate']['z']))
 #           print (singleData)
            
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
            actor["Rotation"] = str(GIS.DegreeToRadian(singleData['courseAngle']))
            actor["PositionZ"] = str(singleData['coordinate']['z']+0.9)
            actor["PositionX"] = str(out.x)
            actor["PositionY"] = str(out.y)
            print('ready to send:' + str(actor))
            try:
                socket.send((json.dumps(actor) + '@').encode('utf-8'))
            except:
                print('traffic provider is closed: ' + str(singleData['timestamp']))
 
loop = asyncio.get_event_loop()
loop.run_until_complete(main())