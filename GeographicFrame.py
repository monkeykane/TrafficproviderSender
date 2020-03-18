from GIS import GIS
import CartesianCoordinateSystem
import math
from Vector3 import Vector3

class GeographicFrameEnu():
    def __init__(self, orilat, orilon, orialt):
        ecef = GIS.WGSToEarthCenterXYZ(orilat,orilon,orialt)
        self.coord = GIS.BuildEnuCoordinateSystem(ecef)
    
    def WgsToLocal(self, lat, lon, alt):
        ecef = GIS.WGSToEarthCenterXYZ(lat, lon, alt)
        return self.coord.WorldToLocal(ecef)