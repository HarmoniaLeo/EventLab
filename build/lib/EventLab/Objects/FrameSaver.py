import numpy as np
import scipy.io
import cv2

class FrameSaver:

    def __init__(self,Frame):
        if Frame==None:
            raise Exception("Frame data isn't available.")
        self._Frame=Frame
        self._Frame.readFromStartStamp()

class FrameToIndex(FrameSaver):
    def save(self,directionOfImgs,directionOfIndex=None):
        if directionOfIndex!=None:
            f=open(directionOfIndex,mode="wb")
        data=[None,None]
        i=0
        num=self._Frame.getLength()
        while num>1:
            num/=10
            i+=1
        j=0
        while self._Frame.readData(data):
            name=str(j).rjust(i,'0')
            name+=".png"
            if directionOfIndex!=None:
                f.write("{0} {1}\n".format(data[0],name).encode("utf-8"))
            cv2.imwrite(directionOfImgs+"/"+name,np.array(data[1]).astype(np.uint8))
            j+=1
        if directionOfIndex!=None:
            f.close()

class FrameToMat(FrameSaver):
    def save(self,direction):
        data=[None,None]
        timeStamps=np.empty(0)
        imgs=np.empty(0)
        while self._Frame.readData(data):
            timeStamps=np.append(timeStamps,[data[0]])
            imgs=np.append(imgs,[data[1]])
        matrix=np.array([timeStamps,imgs])
        scipy.io.savemat(direction,{'Frame':matrix})

class FrameToVideo(FrameSaver):
    def save(self,direction,fr):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(direction,fourcc, fr, self._Frame.getSize(),True)
        data=[None,None]
        while self._Frame.readData(data):
            img=data[1]
            img=cv2.cvtColor(np.uint8(img),cv2.COLOR_GRAY2BGR)
            out.write(img)
        out.release()