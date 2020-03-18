import time
import json
import socket

if __name__ == '__main__':
    trafficProviderSocket = socket.socket()
    trafficProviderSocket.connect(("127.0.0.1", 21568))
    print("start data process node...\n")
    print("connect traffic provider ip: 127.0.0.1 port:21568")

    tick = 0
    pulse = 0.001
    t=0
    while True:
        start = time.time()
        s=[1,2,3,4,5,6,7,8]
        
        for index in range(len(s)):
            actor = {}
            actor["Time"] = str(tick)
            actor["Speed"] = str(0)
            actor["ID"] = str(index)
            actor["AssetID"] = str(1000000+index)
            actor["Rotation"] = str(0)
            actor["PositionZ"] = "1"
            x = 8.3 * t
            actor["PositionX"] = str(0)
            actor["PositionY"] = str(0)
            actor["color"] = str(4)
            try:
                trafficProviderSocket.send((json.dumps(actor) + '@').encode('utf-8'))
            except:
                print('traffic provider is closed: ' + str(time.time()))

        end = time.time()
        if pulse > (end - start):
            time.sleep(pulse - (end - start))
        tick = tick + pulse
        t += pulse