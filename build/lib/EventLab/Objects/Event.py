import linecache
import scipy.io
import pandas as pd
import numpy as np
import pandas as pd


class Event:

    def __init__(self,camera=None,size=None):
        if camera==None and size==None:
            raise Exception("Size hasn't been initialized.")
        if size!=None:
            self.__size=size
        if camera!=None:
            self.__size=camera.getSize()
        self.__event=[]
        self.__point=0
    
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
            event[0]=int(self.__event[self.__point][0])
            event[1]=int(self.__event[self.__point][1])
            event[2]=self.__event[self.__point][2]
            event[3]=int(self.__event[self.__point][3])
            self.__point+=1
            return True
    
    def readFromStartStamp(self):
        self.__point=0
    
    def addData(self,x,y,ts,p):
        if ts<0:
            raise Exception("Illegal timestamp.")
        if len(self.__event)==0:
            self.__event.append([x,y,ts,p])
            return
        if ts<=self.__event[0][2]:
            self.__event.insert(0,[x,y,ts,p])
            return
        for i in range(0,len(self.__event)-1):
            if ts>self.__event[i][2] and ts<self.__event[i+1][2]:
                self.__event.insert(i+1,[x,y,ts,p])
                return
        self.__event.append([int(x),int(y),ts,int(p)])
    
    def setData(self,arr):
        self.__event=arr
    
    def getSize(self):
        return self.__size
    
class EventFromText(Event):

    def __init__(self,camera,size,direction,xRow,yRow,timeStampRow,polarityRow,splitSymbol,startStamp,endStamp):
        super().__init__(camera,size)
        f=open(direction)
        dataLines=f.readlines()
        for i in range(0,len(dataLines)):
            dataLines[i]=dataLines[i][:-1].split(splitSymbol)
        data=np.array(dataLines)
        xs=data[...,xRow].astype(np.int_)
        ys=data[...,yRow].astype(np.int_)
        tss=data[...,timeStampRow].astype(np.float_)
        indexs=np.where((tss>=startStamp)&(tss<=endStamp))
        ps=data[...,polarityRow].astype(np.int_)
        xs=xs[indexs]
        ys=ys[indexs]
        tss=tss[indexs]
        ps=ps[indexs]
        self.setData(np.array([xs,ys,tss,ps]).T.tolist())
        f.close()

class EventFromMat(Event):
    def __init__(self,camera,size,field,indexList,direction,xRow,yRow,timeStampRow,polarityRow,splitSymbol,startStamp,endStamp):
        super().__init__(camera,size)
        data=[]
        data=scipy.io.loadmat(direction)[field]
        try:
            data=scipy.io.loadmat(direction)[field]
            for i in indexList:
                data=data[i]
        except Exception:
            raise Exception("Illegal direction or index.")
        xs=data[xRow].T
        ys=data[yRow].T
        tss=data[timeStampRow].T
        ps=data[polarityRow].T
        indexs=np.where((tss>=startStamp)&(tss<=endStamp))
        xs=xs[indexs].astype(np.int_)
        ys=ys[indexs].astype(np.int_)
        tss=tss[indexs]
        ps=ps[indexs].astype(np.int_)
        self.setData(np.array([xs,ys,tss,ps]).T.tolist())
