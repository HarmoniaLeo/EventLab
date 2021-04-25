import numpy as np
import matplotlib.pyplot as plt
import math
import EventLab.Datas

class SAI:

    def _motionCompensation(self,v,fre,fre_0,d,stamp,reference_time):
        v=(fre/fre_0)*self._size[1]*v/(d*1.25)
        return round((stamp-reference_time)*v)

    def _publish(self,result_img_2):
        return (result_img_2-np.min(result_img_2))/(np.max(result_img_2)-np.min(result_img_2))*255

    def action(self,Event,size,v,fre,fre_0,d,reference_time,lbd,thershold,c_on,c_off):
        Event.readFromStartStamp()
        plt.ion()
        init=False
        event=[0,0,0,0]
        self._size=size
        self._Event=Event
        result_img_2=np.zeros(self._size,dtype=np.float)+0.05
        k=0
        while(self._Event.readData(event)):
            if not init:
                old_event=event.copy()
                init=True
            c=self._motionCompensation(v,fre,fre_0,d,event[2],reference_time)
            flag=(event[1]!=old_event[1])&(event[0]!=old_event[0])
            if(((event[0]+c)<self._size[1])&((event[0]+c)>=0)&(event[1]<self._size[0])&(event[1]>=0)&flag):
                if(event[3]>0):
                    p1=c_on*math.exp(-lbd*result_img_2[event[1],event[0]+c])
                else:
                    p1=c_off*math.exp(lbd*result_img_2[event[1],event[0]+c])
                result_img_2[event[1],event[0]+c]=result_img_2[event[1],event[0]+c]*math.exp(thershold*p1)
            if k%10000==0:
                plt.cla()
                plt.title("Time:"+str(event[2]))
                plt.imshow(self._publish(result_img_2),cmap='gray')
                plt.pause(0.05)
            k+=1
            old_event=event.copy()
        result=EventLab.Datas.getEmptyFrame(self._size)
        result.addData(0,self._publish(result_img_2))
        return result
        

class SAINormal(SAI):

    def action(self,Frame,size,v,fre,fre_0,d,reference_time):
        Frame.readFromStartStamp()
        self._size=size
        self._Frame=Frame
        plt.ion()
        data=[None,None]
        init=False
        result_img_2=np.zeros(self._size,dtype=np.float)+0.05
        k=0
        while(self._Frame.readData(data)):
            if not init:
                result_img_2=data[1]
                k+=1
                init=True
                continue
            img=data[1]
            ts=data[0]
            c=self._motionCompensation(v,fre,fre_0,d,ts,reference_time)
            if c>0:
                img=np.array(img)[...,:self._size[1]-c]
                part1=np.zeros((self._size[0],c))
                img=np.concatenate((part1,img),axis=1)
            else:
                img=np.array(img)[...,-c:]
                part1=np.zeros((self._size[0],-c))
                img=np.concatenate((img,part1),axis=1)
            img=img.astype(np.float_)
            result_img_2=result_img_2*(k/(k+1))+img/(k+1)
            plt.cla()
            plt.subplot(1,2,1)
            plt.imshow(img,cmap='gray')
            plt.subplot(1,2,2)
            plt.imshow(result_img_2,cmap='gray')
            plt.pause(0.5)
            k+=1
        result=EventLab.Datas.getEmptyFrame(self._size)
        result.addData(0,self._publish(result_img_2))
        return result