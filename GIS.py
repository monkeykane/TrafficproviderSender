import math
from Vector3 import Vector3 
from CartesianCoordinateSystem import CartesianCoordinateSystem
from ECEF import ECEF

EPSON = 0.0000000001

class GIS():
    def DegreeToRadian(deg):
        return deg * math.pi / 180
    
    def RadianToDegree(rad):
        return rad * 180 / math.pi
    
    def EarthCenterXYZToWGS(pos):
        geo = ECEF.ecef_to_geo(pos)
        return Vector3(GIS.RadianToDegree(geo.x), GIS.RadianToDegree(geo.y), geo.z)
    
    def WGSToEarthCenterXYZ(latitude, longitude, altitude):
        lat = GIS.DegreeToRadian(latitude)
        lon = GIS.DegreeToRadian(longitude)
        ecef = ECEF.geo_to_ecef(Vector3(lat, lon, altitude))
        return ecef


    def BuildEnuCoordinateSystem_1(v0, vnorth):
        axisZ = v0.normalize()
        axisX = Vector3.crossProduct(vnorth, v0).normalize()
        axisY = Vector3.crossProduct(axisZ, axisX).normalize()
        
        coordSys = CartesianCoordinateSystem()
        coordSys.mCenter = v0
        coordSys.mAxisX = axisX
        coordSys.mAxisY = axisY
        coordSys.mAxisZ = axisZ
        return coordSys
 
    def BuildEnuCoordinateSystem(v0):
        if v0.vectorMag() <= EPSON:
            v0 = Vector3(1,0,0)
        wgs = GIS.EarthCenterXYZToWGS(v0)
        vnorth = GIS.WGSToEarthCenterXYZ(wgs.x+1, wgs.y, wgs.z)
        return GIS.BuildEnuCoordinateSystem_1(v0,vnorth)
    
