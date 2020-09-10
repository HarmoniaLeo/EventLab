from Algorithm import Algorithm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class threeDCloud(Algorithm):
    def action(self):
   
        # 正负极性时间分离
        self._Event.readFromStartStamp()
        x_n=[]
        y_n=[]
        t_n=[]
        x_p=[]
        y_p=[]
        t_p=[]
        event=[0,0,0,0]
        while(self._Event.readData(event)):
            if event[3]>0:
                x_p.append(event[0])
                y_p.append(event[1])
                t_p.append(event[2])
            else:
                x_n.append(event[0])
                y_n.append(event[1])
                t_n.append(event[2])

        # 3维显示筛选后的数据
        fig1 = plt.figure()
        ax1 = Axes3D(fig1)
        ax1.scatter3D(x_n,y_n,t_n,s=1,c='#00CED1')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('time')
    
        fig2 = plt.figure()
        ax2 = Axes3D(fig2)
        ax2.scatter3D(x_p,y_p,t_p,s=1,c='#DC143C')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_zlabel('time')
    
        plt.show()