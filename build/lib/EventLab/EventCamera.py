import EventLab.Objects.Event
import EventLab.Objects.Frame
import EventLab.Objects.Camera
import EventLab.Datas

class EventCamera:
    _Camera=None

    def calibration(self,imgSize,K=[]):
        self._Camera=EventLab.Objects.Camera.calibration(imgSize,K)
    
    def getSize(self):
        return self._Camera.getSize()
    
    def getK(self):
        return self._Camera.getK()

    def getFx(self):
        return self._Camera.getFx()
    
    def getFy(self):
        return self._Camera.getFy()
    
    def getS(self):
        return self._Camera.getS()
    
    def getPx(self):
        return self._Camera.getPx()
    
    def getPy(self):
        return self._Camera.getPy()

    def readEventFromText(self,direction,xRow=1,yRow=2,timeStampRow=0,polarityRow=3,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff):
        return EventLab.Objects.Event.EventFromText(self._Camera,None,direction,xRow,yRow,timeStampRow,polarityRow,splitSymbol,startStamp,endStamp)
    
    def readEventFromMat(self,direction,field="event",indexList=[],xRow=1,yRow=2,timeStampRow=0,polarityRow=3,startStamp=0,endStamp=0x7fffffff):
        return EventLab.Objects.Event.EventFromMat(self._Camera,None,field=field,indexList=indexList,direction=direction,xRow=xRow,yRow=yRow,timeStampRow=timeStampRow,polarityRow=polarityRow,splitSymbol=" ",startStamp=startStamp,endStamp=endStamp)
    
    def readFrameByIndex(self,directionOfIndex,directionOfImages,stampRow=0,imgRow=-1,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        return EventLab.Objects.Frame.FrameByIndex(self._Camera,None,directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol,startStamp,endStamp,startIndex,endIndex)

    def readFrameFromMat(self,direction,field="Frame",indexList=[],timeStampRow=0,imgRow=1,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        return EventLab.Objects.Frame.FrameFromMat(self._Camera,None,field,indexList,direction,timeStampRow,imgRow,startStamp,endStamp,startIndex,endIndex)

    def readFrameFromVideo(self,direction,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        return EventLab.Objects.Frame.FrameFromVideo(self._Camera,None,direction,startStamp,endStamp,startIndex,endIndex)
    
    def DynamicInput(self,direction,startStamp,endStamp):
        return EventLab.Datas.DynamicInput(direction,startStamp,endStamp)
    
def calibration(imgSize,K=[]):
    camera=EventCamera()
    camera.calibration(imgSize,K)
    return camera