import EventLab.Objects.Event
import EventLab.Objects.Frame
import EventLab.Objects.EventSaver
import EventLab.Objects.FrameSaver
import ctypes
import numpy as np
import numpy.ctypeslib as npct
import cv2

def getEmptyEvent(size):
    return EventLab.Objects.Event.Event(None,size)

def readEventFromText(size,direction,xRow=1,yRow=2,timeStampRow=0,polarityRow=3,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff):
    return EventLab.Objects.Event.EventFromText(None,size,direction,xRow,yRow,timeStampRow,polarityRow,splitSymbol,startStamp,endStamp)
    
def readEventFromMat(size,direction,field="event",indexList=[],xRow=1,yRow=2,timeStampRow=0,polarityRow=3,startStamp=0,endStamp=0x7fffffff):
    return EventLab.Objects.Event.EventFromMat(None,size,field=field,indexList=indexList,direction=direction,xRow=xRow,yRow=yRow,timeStampRow=timeStampRow,polarityRow=polarityRow,splitSymbol=" ",startStamp=startStamp,endStamp=endStamp)

def getEmptyFrame(size):
    return EventLab.Objects.Frame.Frame(None,size)

def readFrameByIndex(size,directionOfIndex,directionOfImages,stampRow=0,imgRow=-1,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
    return EventLab.Objects.Frame.FrameByIndex(None,size,directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol,startStamp,endStamp,startIndex,endIndex)

def readFrameFromMat(size,direction,field="Frame",indexList=[],timeStampRow=0,imgRow=1,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
    return EventLab.Objects.Frame.FrameFromMat(None,size,field,indexList,direction,timeStampRow,imgRow,startStamp,endStamp,startIndex,endIndex)

def readFrameFromVideo(size,direction,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1):
    return EventLab.Objects.Frame.FrameFromVideo(None,size,direction,startStamp,endStamp,startIndex,endIndex)

def DynamicInput(direction,startStamp,endStamp):
    p1=ctypes.c_char_p(str("\n"*1024**3).encode("utf-8"))
    p2=ctypes.c_char_p(str("\n"*1024**3).encode("utf-8"))
    p3=ctypes.c_char_p(str("\n"*1024).encode("utf-8"))
    lib = npct.load_library(direction,".")
    lib.startReading.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_double]
    input("Press any key to start reading from camera:")
    lib.startReading(p1,p2,p3,startStamp,endStamp)
    p1=p1.value.decode("utf-8")
    p2=p2.value.decode("utf-8")
    p3=p3.value.decode("utf-8")
    p1=p1.split("\n")
    for i in range(0,len(p1)):
        if p1[i]=='':
            break
        p1[i]=p1[i].split(" ")
        p1[i][0]=int(p1[i][0])
        p1[i][1]=int(p1[i][1])
        p1[i][2]=float(p1[i][2])
        p1[i][3]=int(p1[i][3])
    p2=p2.split("\n")
    p3=p3.split("\n")
    ysize=int(p3[1])
    xsize=int(p3[0])
    imgList=[]
    for i in p2:
        if i=='':
            break
        i=i.split(" ")
        l=[None,None]
        l[0]=float(i[0])
        img=np.array(i[1:-1])
        img=img.reshape((ysize,xsize))
        l[1]=img.tolist()
        imgList.append(l)
    Event=getEmptyEvent([ysize,xsize])
    Frame=getEmptyFrame([ysize,xsize])
    Event.setData(p1[:-1])
    Frame.setData(imgList)
    return Event,Frame

def saveEventAsText(event,direction):
    EventLab.Objects.EventSaver.EventToText(event).save(direction)
    
def saveEventAsMat(event,direction):
    EventLab.Objects.EventSaver.EventToMat(event).save(direction)

def saveFrameAsIndex(frame,directionOfImages,directionOfIndex=None):
    EventLab.Objects.FrameSaver.FrameToIndex(frame).save(directionOfImages,directionOfIndex)

def saveOneFrame(frame,directionOfImage):
    data=[None,None]
    frame.readData(data)
    cv2.imwrite(directionOfImage,np.array(data[1]).astype(np.uint8))

def saveFrameAsMat(frame,direction):
    EventLab.Objects.FrameSaver.FrameToMat(frame).save(direction)

def saveFrameAsVideo(frame,direction,frameRate):
    EventLab.Objects.FrameSaver.FrameToVideo(frame).save(direction,frameRate)