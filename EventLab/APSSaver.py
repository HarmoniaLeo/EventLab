import numpy as np
import scipy.io
import cv2

class APSSaver:
    _APS=None

    def __init__(self,aps):
        if aps==None:
            raise Exception("APS data isn't available.")
        self._APS=aps

class APSToIndex(APSSaver):
    def save(self,directionOfIndex,directionOfImgs):
        f=open(directionOfIndex,mode="wb")
        data=[None,None]
        i=0
        num=self._APS.getLength()
        while num>1:
            num/=10
            i+=1
        j=0
        while self._APS.readData(data):
            name=str(j).rjust(i,'0')
            name+=".png"
            f.write("{0} {1}\n".format(data[0],name),encode="utf-8")
            cv2.imwrite(directionOfImgs+"/"+name)
            j+=1
        f.close()

class APSToMat(APSSaver):
    def save(self,direction):
        data=[None,None]
        timeStamps=np.empty(0)
        imgs=np.empty(0)
        while self._APS.readData(data):
            timeStamps=np.append(timeStamps,[data[0]])
            imgs=np.append(imgs,[data[1]])
        matrix=np.array([timeStamps,imgs])
        scipy.io.savemat(direction,{'APS':matrix})

class APSToVideo(APSSaver):
    def save(self,direction,fr):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(direction,fourcc, fr, self._APS.getSize(),True)
        data=[None,None]
        while self._APS.readData(data):
            img=data[1]
            out.write(img)
        out.release()