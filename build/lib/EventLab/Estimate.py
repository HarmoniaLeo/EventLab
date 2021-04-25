import EventLab.Algorithms.EstimateAlgorithm

def getSSIM(frame,groundTruth,bins=10):
    EventLab.Algorithms.EstimateAlgorithm.ssim().action(groundTruth,frame,bins)
    
def getPSNR(frame,groundTruth,bins=10):
    EventLab.Algorithms.EstimateAlgorithm.psnr().action(groundTruth,frame,bins)