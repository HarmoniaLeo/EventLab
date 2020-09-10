from EventLab.Algorithm import AlgorithmWithAPS
import numpy as np
import cv2
import matplotlib.pyplot as plt

class ComplementaryFilter(AlgorithmWithAPS):
    __L0=0
    __LF=0
    __preStamp=0
    __alpha=0
    __pcMap=0
    __mcMap=0
    __pCountMap=0
    __mCountMap=0
    __count=0

    def __init__(self,event,aps,camera):
        super().__init__(event,aps,camera)

    def __initialize(self,eventData,apsData,alpha1,stamp):
        img_size=self._Camera.getSize()
        self.__L0=np.zeros(img_size,dtype=np.float)
        self.__LF=np.zeros(img_size,dtype=np.float)
        if(self._Event.readData(eventData) and self._APS.readData(apsData)):
            self.__preStamp=np.zeros(img_size)+stamp
            self.__alpha=np.zeros(img_size)+alpha1
            self.__pcMap=np.zeros(img_size)
            self.__mcMap=np.zeros(img_size)
            self.__pCountMap=np.zeros(img_size)
            self.__mCountMap=np.zeros(img_size)
            self.__count=0
            return np.min((eventData[2],apsData[1]))
        else:
            return -1

    def __eventsCallback(self,eventData,pc,mc):
        x=eventData[0]
        y=eventData[1]
        ts=eventData[2]
        p=eventData[3]
        beta=np.exp(-1*self.__alpha[y,x]*(ts-self.__preStamp[y,x]))
        if p>0:
            c=pc
            self.__pCountMap[y,x]+=1
        else:
            c=-mc
            self.__mCountMap[y,x]+=1
        self.__L0[y,x]=beta*self.__L0[y,x]+(1-beta)*self.__LF[y,x]+c
        self.__preStamp[y,x]=ts

    def __apsCallback(self,apsData,L):
        imgNow=np.log(apsData[0].astype(np.float_)/255+1)
        self.__updateC(imgNow)
        del self.__LF
        self.__LF=imgNow
        self.__updateAlpha(L)
    
    def __updateC(self,imgNow):
        img_size=self._Camera.getSize()
        diffImg=imgNow-self.__LF
        change=self.__pCountMap-self.__mCountMap
        thershold=np.zeros(img_size)
        '''
        logApsChangeMin=0.03
        dvsChangeMin=2
        onoffRatioMin=2

        diffImg=imgNow-self.__LF
        change=self.__pCountMap-self.__mCountMap
        ratio=(self.__pCountMap+1e-6)/(self.__mCountMap+1e-6)
        eventCountOnMax=np.percentile(self.__pCountMap,99.5)
        eventCountOffMax=np.percentile(self.__mCountMap,99.5)

        thershold=np.zeros(img_size)
        thershold=np.where((diffImg>logApsChangeMin)&(change>dvsChangeMin)\
            &(ratio>onoffRatioMin)&(self.__pCountMap<eventCountOnMax)&(change!=0),\
            diffImg/change,thershold)
        thershold=np.where((diffImg<-logApsChangeMin)&(change<-dvsChangeMin)\
            &(ratio<1/onoffRatioMin)&(self.__mCountMap<eventCountOffMax)&(change!=0),\
            -diffImg/change,thershold)
        '''
        
        thershold=np.where(diffImg>0,diffImg/change,thershold)
        thershold=np.where(diffImg<0,diffImg/change,thershold)
        thershold=np.where(change==0,0,thershold)
        beta=np.power(1-0.95,0.1)
        self.__pcMap=np.where(diffImg>0,beta*self.__pcMap+(1-beta)*thershold,self.__pcMap)
        self.__mcMap=np.where(diffImg<0,beta*self.__mcMap+(1-beta)*thershold,self.__mcMap)
        del thershold
        del self.__pCountMap
        del self.__mCountMap
        self.__pCountMap=np.zeros(img_size)
        self.__mCountMap=np.zeros(img_size)


    def __updateAlpha(self,L):
        self.__alpha=np.where(self.__LF<L,0.1*self.__alpha+0.9*self.__alpha*self.__LF/L,self.__alpha)
        self.__alpha=np.where(self.__LF>np.log(2)-L,self.__alpha,0.1*self.__alpha-0.9*self.__alpha*(self.__LF-np.log(2))/L)

    def __publish(self,dir,stamp):
        '''
        img_size=self._Camera.getSize()
        beta=np.exp(-1*self.__alpha*(stamp-self.__preStamp))
        self.__L0=beta*self.__L0+(1-beta)*self.__LF
        del self.__preStamp
        self.__preStamp=np.zeros(img_size)+stamp
        '''
        img=(np.exp(self.__L0)-1)*255
        cv2.imwrite(dir+'/'+"{0:04d}".format(self.__count)+'.png',img)
        self.__count+=1

    def action(self,rebuildFramRate,outputDir,alpha1,pc,mc,L):
        apsData=[0,0]
        eventData=[0,0,0,0]
        init=False
        nextBuildStamp=0
        stamp=0
        while self._Event.readData(eventData):
            if not init:
                if self._APS.readData(apsData):
                    stamp=np.min((eventData[2],apsData[1]))
                    self.__initialize(eventData,apsData,alpha1,stamp)
                    nextBuildStamp=np.min((eventData[2],apsData[1]))+1/rebuildFramRate
                else:
                    break
                init=True
            img_size=self._Camera.getSize()
            beta=np.exp(-1*self.__alpha*(stamp-self.__preStamp))
            self.__L0=beta*self.__L0+(1-beta)*self.__LF
            del self.__preStamp
            self.__preStamp=np.zeros(img_size)+stamp
            if eventData[2]<=apsData[1]:
                stamp=eventData[2]
                self.__eventsCallback(eventData,pc,mc)
            else:
                stamp=apsData[1]
                self.__apsCallback(apsData,L)
                pc=np.average(self.__pcMap!=0)
                mc=np.average(self.__mcMap!=0)
                if not self._APS.readData(apsData):
                    break
            if stamp>nextBuildStamp:
                self.__publish(outputDir,stamp)
                nextBuildStamp+=1/rebuildFramRate