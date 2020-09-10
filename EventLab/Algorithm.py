class Algorithm:
    _Event=None
    _Camera=None

    def __init__(self,event,camera):
        if camera==None:
            raise Exception("Camera hasn't benn calibrated.")
        if event==None:
            raise Exception("Event data isn't available.")
        self._Event=event
        self._Event.readFromStartStamp()
        self._Camera=camera

class AlgorithmWithAPS:
    _Event=None
    _APS=None
    _Camera=None

    def __init__(self,event,aps,camera):
        if event==None:
            raise Exception("Event data isn't available.")
        if camera==None:
            raise Exception("Camera isn't available.")
        if aps==None:
            raise Exception("APS data isn't available.")
        self._Event=event
        self._Event.readFromStartStamp()
        self._APS=aps
        self._APS.readFromStartStamp()
        self._Camera=camera