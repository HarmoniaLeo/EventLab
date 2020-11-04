import matplotlib.pyplot as plt
import numpy as np

class BuildFrame:
    def action(self,event,frame,size,exposureTime,showTime):
        event.readFromStartStamp()
        frame.readFromStartStamp()
        plt.figure()
        plt.subplot(2, 1, 1).set_title("event frame")
        plt.subplot(2,1,2).set_title("aps frame")
        eventData=[0,0,0,0]
        apsData=[0,0]
        while(frame.readData(apsData)):
            eventFrame=np.stack((np.zeros(size)+255,np.zeros(size)+255,np.zeros(size)+255),axis=2)
            apsFrame=apsData[0]
            while(event.readData(eventData)):
                if(eventData[2]>apsData[1] and eventData[2]<apsData[1]+exposureTime):
                    x=eventData[0]
                    y=eventData[1]
                    if eventData[3]==0:
                        eventFrame[y,x,0]=0
                        eventFrame[y,x,1]=0
                    else:
                        eventFrame[y,x,1]=0
                        eventFrame[y,x,2]=0
                if(eventData[2]>=apsData[1]+exposureTime):
                    break
            plt.subplot(1,2,1).imshow(eventFrame)
            plt.subplot(1,2,2).imshow(apsFrame,cmap="gray")
            plt.pause(showTime)
            del eventFrame
            del apsFrame

class BuildFrameWithTs:
    def action(self,event,size,showTime,frameRate):
        event.readFromStartStamp()
        eventData=[0,0,0,0]
        plt.ion()
        while(event.readData(eventData)):
            eventFrame=np.stack(np.stack(np.zeros(size)+255,np.zeros(size)+255,np.zeros(size)+255),axis=2)
            timeNow=eventData[2]
            while(True):
                if(eventData[2]>=timeNow+1/frameRate):
                    break
                x=eventData[0]
                y=eventData[1]
                if eventData[3]==0:
                    eventFrame[y,x,0]=0
                    eventFrame[y,x,1]=0
                else:
                    eventFrame[y,x,1]=0
                    eventFrame[y,x,2]=0
                event.readData(eventData)
            plt.imshow(eventFrame)
            plt.title("time:"+str(timeNow))
            plt.pause(showTime)
            del eventFrame