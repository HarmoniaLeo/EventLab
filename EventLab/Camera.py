class Camera:
    _picSize=[None,None]
    _K=[]
    
    def __init__(self,picSize,K):
        self._picSize=picSize
        self._K=K
        
    def getSize(self):
        return self._picSize
    
    def getK(self):
        return self._K

    def getFx(self):
        return self._K[0][0]
    
    def getFy(self):
        return self._K[1][1]
    
    def getS(self):
        return self._K[0][1]
    
    def getPx(self):
        return self._K[0][2]
    
    def getPy(self):
        return self._K[1][2]