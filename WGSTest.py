from GeographicFrame import GeographicFrameEnu


ORILAT=31.2828880548475
ORILON=121.171131134033
ORIALT=0

if __name__ == '__main__':
    frameEnu = GeographicFrameEnu(ORILAT,ORILON,ORIALT)
    out = frameEnu.WgsToLocal(31.283209, 121.16905, 0)
    print(out.x, out.y)