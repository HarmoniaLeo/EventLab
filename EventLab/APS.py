import linecache
import scipy.io
import cv2
import os
import numpy as np

class APS:
    __datas=[]
    __point=0
    __size=None

    def __init__(self,camera,size):
        if camera==None and size==None:
            raise Exception("Camera hasn't benn calibrated.")
        if size!=None:
            self.__size=size
        if camera!=None:
            self.__size=camera.getSize()

    def _checkTimeStampAndIndex(self,ts,startStamp,endStamp,i,startIndex,endIndex):
        if endStamp<=startStamp:
            raise Exception("Illegal timestamp.")
        if endIndex>=0 and startIndex>=0 and endIndex<=startIndex:
            raise Exception("Illegal index.")
        if ((endIndex<0 and ts<=endStamp) or (endIndex>0 and i<=endIndex)) and ((startIndex<0 and ts>=startStamp) or (endIndex>0 and i>=startIndex)):
            return True
        return False
    
    def readData(self,data):
        if self.__point>=len(self.__datas):
            return False
        else:
            data[0]=self.__datas[self.__point][0]
            data[1]=self.__datas[self.__point][1]
            self.__point+=1
            return True

    def readDataOnN(self,n):
        if n>=len(self.__datas):
            raise Exception("Illegal index")
        else:
            return self.__datas[n][0],self.__datas[n][1]
    
    def readFromStartStamp(self):
        self.__point=0
    
    def addData(self,ts,img):
        if img.shape!=self.__size:
            raise Exception("APS data size error.")
        if ts<0:
            raise Exception("Illegal timestamp.")
        if ts<self.__datas[0][0]:
            self.__datas.insert(0,[ts,img])
            return
        for i in range(0,len(self.__datas)-1):
            if ts==self.__datas[i][0] or ts==self.__datas[i+1][0]:
                raise Exception("Illegal timestamp.")
            if ts>self.__datas[i][0] and ts<self.__datas[i+1][0]:
                self.__datas.insert(i+1,[ts,img])
                return
        self.__datas.append([ts,img])
    
    def getLength(self):
        return len(self.__datas)
    
    def getSize(self):
        return self.__size


class APSByIndex(APS):

    def __init__(self,camera,size,directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol,startStamp,endStamp,startIndex,endIndex):
        super().__init__(camera,size)
        f=open(directionOfIndex)
        ts=0
        i=0
        if imgRow<0:
            imgList=os.listdir(directionOfImages)
        while True:
            dataLine=f.readline()
            if dataLine=="":
                break
            dataLine=dataLine[:-1].split(splitSymbol)
            ts=float(dataLine[stampRow])
            if self._checkTimeStampAndIndex(ts,startStamp,endStamp,i,startIndex,endIndex):
                if imgRow>=0:
                    gray_img=cv2.imread(directionOfImages+"/"+dataLine[imgRow],cv2.IMREAD_GRAYSCALE)
                else:
                    gray_img=cv2.imread(directionOfImages+"/"+imgList[i],cv2.IMREAD_GRAYSCALE)
                self.addData(ts,gray_img)
                i+=1
        f.close()

class APSFromMat(APS):
    
    def __init__(self,camera,size,direction,field,indexList,timeStampRow,imgRow,startStamp,endStamp,startIndex,endIndex):
        super().__init__(camera,size)
        data=[]
        try:
            data=scipy.io.loadmat(direction)[field]
            for i in indexList:
                data=data[i]
        except Exception:
            raise Exception("Illegal direction or mat.")
        num=data[timeStampRow].shape[0]
        for i in range(0,num):
            ts=float(data[timeStampRow][i][0])
            if self._checkTimeStampAndIndex(ts,startStamp,endStamp,i,startIndex,endIndex):
                img=data[imgRow][i][0]
                self.addData(ts,img)

class APSFromVideo(APS):
    
    def __init__(self,camera,size,direction,startStamp,endStamp,startIndex,endIndex):
        super().__init__(camera,size)
        try:
            cap=cv2.VideoCapture(direction)
        except Exception:
            raise Exception("Illegal direction or video.")
        fr=cap.get(5)
        ts=0
        i=0
        while(cap.isOpened()):
            if self._checkTimeStampAndIndex(ts,startStamp,endStamp,i,startIndex,endIndex):
                ret, img = cap.read()
                if img.shape!=camera.getSize():
                    raise Exception("APS data size error.")
                self.addData(ts,img)
            ts+=1/fr
            i+=1
        cap.release()