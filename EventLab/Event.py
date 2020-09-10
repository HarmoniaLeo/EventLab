import linecache
import scipy.io
import pandas as pd
import numpy as np

class Event:
    __event=[]
    __point=0
    __size=None

    def __init__(self,camera,size):
        if camera==None and size==None:
            raise Exception("Camera hasn't benn calibrated.")
        if size!=None:
            self.__size=size
        if camera!=None:
            self.__size=camera.getSize()
    
    def _checkTimeStamp(self,ts,startStamp,endStamp):
        if startStamp>=endStamp:
            raise Exception("Illegal timestamp.")
        if ts>=startStamp and ts<=endStamp:
            return True
        return False

    
    def readData(self,event):
        if self.__point>=len(self.__event):
            return False
        else:
            event[0]=self.__event[self.__point][0]
            event[1]=self.__event[self.__point][1]
            event[2]=self.__event[self.__point][2]
            event[3]=self.__event[self.__point][3]
            self.__point+=1
            return True
    
    def readFromStartStamp(self):
        self.__point=0
    
    def addData(self,x,y,ts,p):
        if ts<0:
            raise Exception("Illegal timestamp.")
        if len(self.__event)==0:
            self.__event.append([x,y,ts,p])
        if ts<=self.__event[0][0]:
            self.__event.insert(0,[x,y,ts,p])
            return
        for i in range(0,len(self.__event)-1):
            if ts>self.__event[i][0] and ts<=self.__event[i+1][0]:
                self.__event.insert(i+1,[x,y,ts,p])
                return
        self.__event.append([x,y,ts,p])
    
class EventFromText(Event):
    def __init__(self,camera,size,direction,xRow,yRow,timeStampRow,polarityRow,splitSymbol,startStamp,endStamp):
        super().__init__(camera,size)
        f=open(direction)
        ts=0
        while True:
            dataLine=f.readline()
            if dataLine=="":
                break
            dataLine=dataLine[:-1].split(splitSymbol)
            ts=float(dataLine[timeStampRow])
            if self._checkTimeStamp(ts,startStamp,endStamp):
                x=int(dataLine[xRow])
                y=int(dataLine[yRow])
                p=int(dataLine[polarityRow])
                self.addData(x,y,ts,p)
        f.close()

class EventFromMat(Event):

    def __init__(self,camera,size,field,indexList,direction,xRow,yRow,timeStampRow,polarityRow,splitSymbol,startStamp,endStamp):
        super().__init__(camera,size)
        data=[]
        try:
            data=scipy.io.loadmat(direction)[field]
            for i in indexList:
                data=data[i]
        except Exception:
            raise Exception("Illegal direction or index.")
        num=data[timeStampRow].shape[0]
        for i in range(0,num):
            ts=float(data[timeStampRow][i][0])
            if self._checkTimeStamp(ts,startStamp,endStamp):
                x=int(data[xRow][i][0])
                y=int(data[yRow][i][0])
                p=int(data[polarityRow][i][0])
                self.addData(x,y,ts,p)