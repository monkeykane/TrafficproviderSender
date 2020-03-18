import math
from Vector3 import Vector3

a = 6378137.0; #WGS-84 semi-major axis
e2 = 6.6943799901377997e-3; #WGS-84 first eccentricity squared
a1 = 4.2697672707157535e+4; #a1 = a*e2
a2 = 1.8230912546075455e+9; #a2 = a1*a1
a3 = 1.4291722289812413e+2; #a3 = a1*e2/2
a4 = 4.5577281365188637e+9; #a4 = 2.5*a2
a5 = 4.2840589930055659e+4; #a5 = a1+a3
a6 = 9.9330562000986220e-1; #a6 = 1-e2
EPSON = 0.0000000001
class ECEF():

    #Convert Earth-Centered-Earth-Fixed (ECEF) to lat, Lon, Altitude
	#Input is a three element array containing x, y, z in meters
	#Returned array contains lat and lon in radians, and altitude in meters
    def ecef_to_geo(ecef):
        zp=w2=w=r2=r=s2=c2=s=c=ss= 0
        g=rg=rf=u=v=m=f=p=x=y=z = 0
        geo = Vector3(0,0,0)
        x = ecef.x
        y = ecef.y
        z = ecef.z
        zp = abs(z)
        w2 = x * x + y * y
        w = math.sqrt(w2)
        r2 = w2 + z * z
        if r2 < EPSON:
            return Vector3(0,0,0)

        r = math.sqrt(r2)
        geo.y = math.atan2(y, x); #Lon (final)
        s2 = z * z / r2
        c2 = w2 / r2
        u = a2 / r
        v = a3 - a4 / r
        if c2 > 0.3:
        	s = (zp / r) * (1.0 + c2 * (a1 + u + s2 * v) / r)
        	geo.x = math.asin(s) #Lat
        	ss = s * s
        	c = math.sqrt(1.0 - ss)
        	
        else:
        	c = (w / r) * (1.0 - s2 * (a5 - u - c2 * v) / r)
        	geo.x = math.acos(c) #Lat
        	ss = 1.0 - c * c
        	s = math.sqrt(ss)
        	
        g = 1.0 - e2 * ss
        rg = a / math.sqrt(g)
        rf = a6 * rg
        u = w - rg * c
        v = zp - rf * s
        f = c * u + s * v
        m = c * v - s * u
        p = m / (rf / g + f)
        geo.x = geo.x + p #Lat
        geo.z = f + m * p / 2.0 #Altitude
        if z < 0.0:
        	geo.x *= -1.0 #Lat
        
        return geo #Return Lat, Lon, Altitude in that order        
    
    #Convert Lat, Lon, Altitude to Earth-Centered-Earth-Fixed (ECEF)
	#Input is a three element array containing lat, lon (rads) and alt (m)
	#Returned array contains x, y, z in meters    
    def geo_to_ecef(geo):
        n, lat, lon, alt = 0,0,0,0
        ecef = Vector3(0,0,0) #Results go here (x, y, z)
        lat = geo.x
        lon = geo.y
        alt = geo.z
        n = a / math.sqrt(1 - e2 * math.sin(lat) * math.sin(lat))
        ecef.x = (n + alt) * math.cos(lat) * math.cos(lon) #ECEF x
        ecef.y = (n + alt) * math.cos(lat) * math.sin(lon) #ECEF y
        ecef.z = (n * (1 - e2) + alt) * math.sin(lat) #ECEF z
        return ecef #Return x, y, z in ECEF