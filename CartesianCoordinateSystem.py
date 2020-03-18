import math
from Vector3 import Vector3

class CartesianCoordinateSystem():
    def __init__(self):
        self.mAxisX = Vector3(1,0,0)
        self.mAxisY = Vector3(0,1,0)
        self.mAxisZ = Vector3(0,0,1)
        self.mCenter = Vector3(0,0,0)
    
    def WorldToLocal(self, p):
        p = p-self.mCenter
        return Vector3(Vector3.dotProduct(p,self.mAxisX),Vector3.dotProduct(p,self.mAxisY),Vector3.dotProduct(p,self.mAxisZ))