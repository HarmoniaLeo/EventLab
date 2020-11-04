import numpy as np
import matplotlib.pyplot as plt
import math

class EstimateAlgorithm:
    def __init__(self):
        self.__measures=np.empty(0)
    
    def _calculate(self,groundTruth,target):
        return None

    def action(self,groundTruth,target,bins):
        groundTruth.readFromStartStamp()
        target.readFromStartStamp()
        data1=[None,None]
        while groundTruth.readData(data1):
            target.readFromStartStamp()
            data2=[None,None]
            while target.readData(data2):
                if data1[0]==data2[0]:
                    self.__measures=np.append(self.__measures,self._calculate(data1[1],data2[1]))
                elif data1[0]<data2[0]:
                    break
        min=np.min(self.__measures)
        max=np.max(self.__measures)
        arr=np.linspace(min,max+1,bins)
        plt.hist(self.__measures,arr,alpha=0.5)
        plt.title("E={0},D={1}".format(np.average(self.__measures),np.std(self.__measures)**2))
        plt.grid(linestyle="-.",axis="both")
        plt.show()

class ssim(EstimateAlgorithm):
    def __init__(self):
        super().__init__()

    def _calculate(self,groundTruthImg,apsImg):
        l=255
        k1=0.01
        k2=0.03
        c1=(k1*l)**2
        c2=(k2*l)**2
        groundTruthImg=np.ravel(groundTruthImg)
        apsImg=np.ravel(apsImg)
        ux=np.average(groundTruthImg)
        uy=np.average(apsImg)
        cmat=np.cov([apsImg,groundTruthImg])
        varx=cmat[1][1]
        vary=cmat[0][0]
        varxy=cmat[1][0]
        print("ssim:{0}".format((2*ux*uy+c1)*(2*varxy+c2)/((ux**2+uy**2+c1)*(varx+vary+c2))))
        return (2*ux*uy+c1)*(2*varxy+c2)/((ux**2+uy**2+c1)*(varx+vary+c2))


class psnr(EstimateAlgorithm):
    def __init__(self):
        super().__init__()
    
    def _calculate(self,img1,img2):
        mse = np.mean((img1 - img2) ** 2 )
        if mse < 1.0e-10:
            return 100
        print("psnr:{0}".format(10 * math.log10(255.0**2/mse)))
        return 10 * math.log10(255.0**2/mse)