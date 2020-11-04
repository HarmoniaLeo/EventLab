import EventLab.Algorithms.ComplementaryFilter
import EventLab.Algorithms.SAI

def ComplementaryFilterAlgorithm(event,frame,rebuildFrameRate,alpha1,pc,mc,L):
    return EventLab.Algorithms.ComplementaryFilter.ComplementaryFilter().action(event,frame,event.getSize(),rebuildFramRate,alpha1,pc,mc,L)

def SAI(event,v,fre,fre_0,d,reference_time,lbd,thershold,c_on,c_off):
    return EventLab.Algorithms.SAI.SAI().action(event,event.getSize(),v,fre,fre_0,d,reference_time,lbd,thershold,c_on,c_off)

def SAINormal(frame,v,fre,fre_0,d,reference_time):
    return EventLab.Algorithms.SAI.SAINormal().action(frame,frame.getSize(),v,fre,fre_0,d,reference_time)