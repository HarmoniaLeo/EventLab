from Event import Event,EventFromText,EventFromMat
from APS import APS,APSByIndex,APSFromMat,APSFromVideo
from APSSaver import APSToIndex,APSToMat,APSToVideo
from EventSaver import EventToText,EventToMat
from Camera import Camera
from BuildFrame import BuildFrame
from threeDCloud import threeDCloud
from Estimate import ssim,psnr

class EventCamera:
    _Event=None
    _APS=None
    _Camera=None
    _EventResult=None
    _APSResult=None
    _GroundTruth=None

    def calibration(self,imgSize,K=[]):
        self._Camera=Camera(imgSize,K)

    def readEventFromText(self,direction,xRow=1,yRow=2,timeStampRow=0,polarityRow=3,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff):
        self._Event=EventFromText(self._Camera,None,direction,xRow,yRow,timeStampRow,splitSymbol,polarityRow,startStamp,endStamp)
    
    def readEventFromMat(self,direction,field="event",indexList=[],xRow=1,yRow=2,timeStampRow=0,polarityRow=3,startStamp=0,endStamp=0x7fffffff):
        self._Event=EventFromMat(self._Camera,None,direction,field,indexList,xRow,yRow,timeStampRow," ",polarityRow,startStamp,endStamp)
    
    def readAPSByIndex(self,directionOfIndex,directionOfImages,stampRow=0,imgRow=-1,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._APS=APSByIndex(self._Camera,None,directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol,startStamp,endStamp,startIndex,endIndex)

    def readAPSFromMat(self,direction,field="APS",indexList=[],timeStampRow=0,imgRow=1,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._APS=APSFromMat(self._Camera,None,direction,field,indexList,timeStampRow,imgRow,startStamp,endStamp,startIndex,endIndex)

    def readAPSFromVideo(self,direction,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._APS=APSFromVideo(self._Camera,None,direction,startStamp,endStamp,startIndex,endIndex)
    
    def saveEventAsText(self,direction):
        EventToText(self._EventResult).save(direction)
    
    def saveEventAsMat(self,direction):
        EventToMat(self._EventResult).save(direction)
    
    def saveAPSAsIndex(self,directionOfIndex,directionOfImages):
        APSToIndex(self._APSResult).save(directionOfIndex,directionOfImages)
    
    def saveAPSAsMat(self,direction):
        APSToMat(self._APSResult).save(direction)
    
    def saveAPSAsVideo(self,direction,frameRate):
        APSToVideo(self._APSResult).save(direction,frameRate)
    
    def readEventResultFromText(self,direction,size,xRow=1,yRow=2,timeStampRow=0,polarityRow=3,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff):
        self._EventResult=EventFromText(None,size,direction,xRow,yRow,timeStampRow,splitSymbol,polarityRow,startStamp,endStamp)
    
    def readEventResultFromMat(self,direction,size,field="event",indexList=[],xRow=1,yRow=2,timeStampRow=0,polarityRow=3,startStamp=0,endStamp=0x7fffffff):
        self._EventResult=EventFromMat(None,size,direction,field,indexList,xRow,yRow,timeStampRow," ",polarityRow,startStamp,endStamp)
    
    def readAPSResultByIndex(self,directionOfIndex,directionOfImages,size,stampRow=0,imgRow=-1,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._APSResult=APSByIndex(None,size,directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol,startStamp,endStamp,startIndex,endIndex)

    def readAPSResultFromMat(self,direction,size,field="APS",indexList=[],timeStampRow=0,imgRow=1,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._APSResult=APSFromMat(None,size,direction,field,indexList,timeStampRow,imgRow,startStamp,endStamp,startIndex,endIndex)

    def readAPSResultFromVideo(self,direction,size,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._APSResult=APSFromVideo(None,size,direction,startStamp,endStamp,startIndex,endIndex)
    
    def readGroundTruthByIndex(self,directionOfIndex,directionOfImages,size,stampRow=0,imgRow=-1,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._GroundTruth=APSByIndex(None,size,directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol,startStamp,endStamp,startIndex,endIndex)

    def readGroundTruthFromMat(self,direction,size,field="APS",indexList=[],timeStampRow=0,imgRow=1,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._GroundTruth=APSFromMat(None,size,direction,field,indexList,timeStampRow,imgRow,startStamp,endStamp,startIndex,endIndex)

    def readGroundTruthFromVideo(self,direction,size,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
        self._GroundTruth=APSFromVideo(None,size,direction,startStamp,endStamp,startIndex,endIndex)
    
    def sourceThreeDCloudShow(self):
        threeDCloud(self._Event,self._Camera).action()
    
    def sourceBuildFrameShow(self,exposureTime,showTime=0.05):
        BuildFrame(self._Event,self._APS,self._Camera).action(exposureTime,showTime)
    
    def resultThreeDCloudShow(self):
        threeDCloud(self._EventResult,self._Camera).action()
    
    def resultBuildFrameShow(self,exposureTime,showTime=0.05):
        BuildFrame(self._EventResult,self._APSResult,self._Camera).action(exposureTime,showTime)
    
    def getSSIM(self,bins=10):
        ssim(self._APS,self._GroundTruth).action(bins)
    
    def getPSNR(self,bins=10):
        psnr(self._APS,self._GroundTruth).action(bins)
    
    