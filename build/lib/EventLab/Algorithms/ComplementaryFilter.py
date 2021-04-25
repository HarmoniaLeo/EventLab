import numpy as np
import cv2
import matplotlib.pyplot as plt
import EventLab.Datas

class ComplementaryFilter:

    def __initialize(self,eventData,frameData,alpha1,stamp,pc,mc,img):
        plt.ion()
        img_size=self._size
        self.__L0=img
        self.__LF=img
        if(self._Event.readData(eventData) and self._frame.readData(frameData)):
            self.__preStamp=np.zeros(img_size)+stamp
            self.__alpha=np.zeros(img_size)+alpha1
            self.__pcMap=np.zeros(img_size)+pc
            self.__mcMap=np.zeros(img_size)+mc
            self.__pCountMap=np.zeros(img_size)
            self.__mCountMap=np.zeros(img_size)
            self.__result=EventLab.Datas.getEmptyFrame(img_size)
            return np.min((eventData[2],frameData[0]))
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
            c=mc
            self.__mCountMap[y,x]+=1
        self.__L0[y,x]=beta*self.__L0[y,x]+(1-beta)*self.__LF[y,x]+c
        self.__preStamp[y,x]=ts

    def __frameCallback(self,frameData,L,alpha1):
        imgNow=np.log(frameData[1].astype(np.float_)/255+1)
        pc,mc=self.__updateC(imgNow)
        del self.__LF
        self.__LF=imgNow
        self.__updateAlpha(L,alpha1)
        return pc,mc
    
    def __updateC(self,imgNow):
        if not self.__updateCInit:
            self.__LF=imgNow
            self.__updateCInit=True
            return np.average(self.__pcMap),np.average(self.__mcMap)
        img_size=self._size

        logIntensityMin=np.log(1+0.15)
        logIntensityMax=np.log(2-0.15)

        logframeChangeMin=0.03
        dvsChangeMin=2
        onoffRatioMin=2

        diffImg=imgNow-self.__LF


        validPixels=np.where((imgNow<logIntensityMax)&(imgNow>logIntensityMin)&(self.__LF<logIntensityMax)&(self.__LF>logIntensityMin))
        diffImg=diffImg[validPixels]

        change=self.__pCountMap-self.__mCountMap+1e-6
        change=change[validPixels]
        ratio=(self.__pCountMap+1e-6)/(self.__mCountMap+1e-6)
        ratio=ratio[validPixels]
        eventCountOnMax=np.percentile(self.__pCountMap,99.5)
        eventCountOffMax=np.percentile(self.__mCountMap,99.5)
        pCountMap=self.__pCountMap[validPixels]
        mCountMap=self.__mCountMap[validPixels]
        pcMap=self.__pcMap[validPixels]
        mcMap=self.__mcMap[validPixels]

        beta=np.power(1-0.95,0.1)
        self.__pcMap[validPixels]=np.where((diffImg>=logframeChangeMin)&(change>=dvsChangeMin)\
            &(ratio>onoffRatioMin)&(pCountMap<eventCountOnMax),\
            beta*pcMap+(1-beta)*(diffImg/change),pcMap)
        self.__mcMap[validPixels]=np.where((diffImg<=-logframeChangeMin)&(change<=-dvsChangeMin)\
            &(ratio<1/onoffRatioMin)&(mCountMap<eventCountOffMax),\
            beta*mcMap+(1-beta)*(-diffImg/change),mcMap)
        del self.__pCountMap
        del self.__mCountMap
        self.__pCountMap=np.zeros(img_size)
        self.__mCountMap=np.zeros(img_size)
        return np.average(self.__pcMap),np.average(self.__mcMap)


    def __updateAlpha(self,L,alpha1):
        minLogframeIntensity=np.log(1)
        maxLogframeIntensity=np.log(2)
        minFraction=0.1
        lowerBound=np.log(1+L)
        upperBound=np.log(2-L)
        saturation=np.zeros_like(self.__alpha)
        saturation=np.where(self.__LF<lowerBound,(minLogframeIntensity-self.__LF)/(minLogframeIntensity-lowerBound),saturation)
        saturation=np.where(self.__LF>upperBound,(maxLogframeIntensity-self.__LF)/(maxLogframeIntensity-upperBound),saturation)
        self.__alpha=np.where((self.__LF<lowerBound)|(self.__LF>upperBound),(minFraction+saturation*(1-minFraction))*alpha1,self.__alpha)

    def __publish(self,stamp):
        #img_size=self._Camera.getSize()
        #beta=np.exp(-1*self.__alpha*(stamp-self.__preStamp))
        #self.__L0=beta*self.__L0+(1-beta)*self.__LF
        #del self.__preStamp
        #self.__preStamp=np.zeros(img_size)+stamp
        img=(np.exp(self.__L0)-1)*255
        img=np.where(img>255,255,img)
        img=np.where(img<0,0,img)
        #plt.imshow(img,cmap='gray')
        #plt.pause(0.005)
        self.__result.addData(stamp,img.astype(np.int8))

    def action(self,event,frame,size,rebuildFramRate,alpha1,pc,mc,L):
        event.readFromStartStamp()
        frame.readFromStartStamp()
        self._Event=event
        self._frame=frame
        self._size=size
        frameData=[0,0]
        eventData=[0,0,0,0]
        init=False
        nextBuildStamp=0
        stamp=0
        while self._Event.readData(eventData):
            if not init:
                if self._frame.readData(frameData):
                    while eventData[2]<=frameData[0]:
                        if not self._Event.readData(eventData):
                            break
                    stamp=np.min((eventData[2],frameData[0]))
                    self.__initialize(eventData,frameData,alpha1,stamp,pc,mc,frameData[1])
                    nextBuildStamp=np.min((eventData[2],frameData[0]))+1/rebuildFramRate
                else:
                    break
                init=True
            #img_size=self._Camera.getSize()
            #beta=np.exp(-1*self.__alpha*(stamp-self.__preStamp))
            #self.__L0=beta*self.__L0+(1-beta)*self.__LF
            #del self.__preStamp
            #self.__preStamp=np.zeros(img_size)+stamp
            if eventData[2]<=frameData[0]:
                stamp=eventData[2]
                self.__eventsCallback(eventData,pc,mc)
            else:
                stamp=frameData[0]
                pc,mc=self.__frameCallback(frameData,L,alpha1)
                if not self._frame.readData(frameData):
                    break
            if stamp>nextBuildStamp:
                self.__publish(stamp)
                nextBuildStamp+=1/rebuildFramRate
        return self.__result