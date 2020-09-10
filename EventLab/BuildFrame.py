import matplotlib.pyplot as plt
import numpy as np
from EventLab.Algorithm import AlgorithmWithAPS

class BuildFrame(AlgorithmWithAPS):

    def action(self,exposureTime,showTime):
        plt.figure()
        plt.subplot(2, 1, 1).set_title("event frame")
        plt.subplot(2,1,2).set_title("aps frame")
        eventData=[0,0,0,0]
        apsData=[0,0]
        while(self._APS.readData(apsData)):
            eventFrame=np.stack((np.zeros(self._Camera.getSize())+255,np.zeros(self._Camera.getSize())+255,np.zeros(self._Camera.getSize())+255),axis=2)
            apsFrame=apsData[0]
            while(self._Event.readData(eventData)):
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
            #eventFrame = eventFrame.transpose((1, 2, 0))
            plt.subplot(1,2,1).imshow(eventFrame)
            plt.subplot(1,2,2).imshow(apsFrame,cmap="gray")
            plt.pause(showTime)
            del eventFrame
            del apsFrame