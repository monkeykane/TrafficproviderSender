import time
import json
import socket
import urllib
import urllib.request
import random
from GeographicFrame import GeographicFrameEnu
from GIS import GIS

ORILAT=31.2828880548475
ORILON=121.171131134033
ORIALT=0
pulse = 0.1
tick = 0
if __name__ == '__main__':
    frameEnu = GeographicFrameEnu(ORILAT,ORILON,ORIALT)
    trafficProviderSocket = socket.socket()
    trafficProviderSocket.connect(("127.0.0.1", 21568))
    print("start data process node...\n")
    print("connect traffic provider ip: 127.0.0.1 port:21568")

    while (True):
        start = time.time()
        # url = "http://120.133.21.14:8090/gqApp/monitor/regionCloud/map?v2xId=210"
        # data = urllib.request.urlopen(url).read()
        # record=data.decode('UTF-8')
        # print(record)
# record -> src_data

        src_data = [{"vid":0,"laneid":"123","coordinate":{"x":121.174954983,"y":31.2827559718,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":325.8426401487822,"speed":14.629141411882237,"vcolor":"ffff00","timestamp":1584525168864},{"vid":30,"laneid":"123","coordinate":{"x":121.169501523,"y":31.2838890275,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":242.7608025632248,"speed":16.321183270511213,"vcolor":"ffff00","timestamp":1584525168969},{"vid":31,"laneid":"123","coordinate":{"x":121.175181846,"y":31.2824431547,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":332.9082029203982,"speed":15.936222640815634,"vcolor":"ffff00","timestamp":1584525168785},{"vid":32,"laneid":"123","coordinate":{"x":121.17094195,"y":31.2844917126,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":166.70078185697204,"speed":10.042704593912946,"vcolor":"ffff00","timestamp":1584525168973},{"vid":33,"laneid":"123","coordinate":{"x":121.175374135,"y":31.2820824119,"z":0.0},"linkid":"123","xacceleration":"3.5","vtype":70,"bearing":"0","wkid":"4326","courseAngle":341.3544058779222,"speed":16.229505861720188,"vcolor":"ffff00","timestamp":1584525168869}]

        json_str=json.dumps(src_data)
        # print(json_str)
        # print(type(json_str))
        #将JSON数据解码为dict（字典）
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
            actor["Time"] = str(tick) #str(singleData['timestamp'])
            actor["Speed"] = str(singleData['speed'])
            actor["ID"] = str(singleData['vid'])
            actor["AssetID"] = str(1000000 + singleData['vid']) #str(random.randint(1000000,1000058))
            actor["Rotation"] = str(GIS.DegreeToRadian(singleData['courseAngle']))
            actor["PositionZ"] = str(singleData['coordinate']['z'] + 0.9)
            actor["PositionX"] = str(out.x)
            actor["PositionY"] = str(out.y)
            # print('ready to send:' + str(actor))
            try:
                trafficProviderSocket.send((json.dumps(actor) + '@').encode('utf-8'))
            except:
                print('traffic provider is closed: ' + str(singleData['timestamp']))
        end = time.time()
        if ( pulse > (end-start)):
            time.sleep(pulse - (end-start)) 
        tick = tick + pulse