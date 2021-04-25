import EventLab.Algorithms.BuildFrame
import EventLab.Algorithms.threeDCloud

def BuildFrame(event,frame,exposureTime=0.05,showTime=0.05):
    return EventLab.Algorithms.BuildFrame.BuildFrame().action(event,frame,event.getSize(),exposureTime,showTime)

def BuildFrameWithTs(event,showTime=0.05,frameRate=10):
    return EventLab.Algorithms.BuildFrame.BuildFrameWithTs().action(event,event.getSize(),showTime,frameRate)

def cloudDisplay(event):
    return EventLab.Algorithms.threeDCloud.threeDCloud().action(event)