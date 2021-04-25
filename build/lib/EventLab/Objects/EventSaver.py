import numpy as np
import scipy.io

class EventSaver:

    def __init__(self,event):
        if event==None:
            raise Exception("Event data isn't available.")
        self._event=event
        self._event.readFromStartStamp()

class EventToText(EventSaver):
    def save(self,direction):
        f=open(direction,mode="wb")
        event=[None,None,None,None]
        while self._event.readData(event):
            f.write("{0} {1} {2} {3}\n".format(event[0],event[1],event[2],event[3]).encode("utf-8"))
        f.close()
    
class EventToMat(EventSaver):
    def save(self,direction):
        event=[None,None,None,None]
        xs=np.empty(0)
        ys=np.empty(0)
        timeStamps=np.empty(0)
        ps=np.empty(0)
        while self._event.readData(event):
            xs=np.append(xs,[event[0]])
            ys=np.append(ys,[event[1]])
            timeStamps=np.append(timeStamps,[event[2]])
            ps=np.append(ps,[event[3]])
        matrix=np.array([xs,ys,timeStamps,ps])
        scipy.io.savemat(direction,{'event':matrix})