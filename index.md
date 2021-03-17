## 1 EventLab库

EventLab库通过对以下对象进行封装与集成，实现了一套**面向对象的事件相机相关应用开发平台**：

1. **相机**（相机各项参数的设置、数据读取）
2. **数据**（包括事件流数据、帧数据）
3. **数据展示算法**
4. **数据处理算法**

其中，**所有对象均提供有可供用户自行继承并拓展的接口**

```python
import EventLab
```

## 2 相机

### 2.1 创建与标定

#### 2.1.1 使用已经取得的内参矩阵

```python
K=[[fx,s,px],[0,fy,py],[0,0,1]]	#创建内参矩阵
imgSize=[y,x]	#设定相机画幅
camera=EventLab.EventCamera.calibration(imgSize,K)	#创建与标定相机对象
camera=EventLab.EventCamera.calibration(imgSize)	#无需考虑相机姿态的应用，可以不使用内参矩阵
```

#### 2.1.2 使用离线数据的张正友标定法

*待开发*

#### 2.1.3 自行开发标定方法

```python
from EventLab.Objects.Camera import Camera

def myCalibration(arg1,arg2,...)	#自行开发的标定方法
	#在该函数中对imgSize=[y,x]（相机画幅）和k=[]（内参矩阵）进行更改
    return Camera(imgSize,k)
```

### 2.2 相机参数使用

| 作用              | 示例                  | 返回值说明                      |
| ----------------- | --------------------- | ------------------------------- |
| 获取画幅          | size=camera.getSize() | size=(y,x)                      |
| 获取内参矩阵      | K=camera.getK()       | K=[[fx,s,px],[0,fy,py],[0,0,1]] |
| 获取x方向焦距     | fx=camera.getFx()     |                                 |
| 获取y方向焦距     | fy=camera.getFy()     |                                 |
| 获取畸变系数      | s=camera.getS()       |                                 |
| 获取x方向主轴偏移 | px=camera.getPx()     |                                 |
| 获取y方向主轴偏移 | py=camera.getPy()     |                                 |

### 2.3 自行开发相机对象

```python
from EventLab.Objects.Camera import Camera

class myCamera(Camera)：
	#在这里添加对Camera的更多实现

def calibrationForMyCamera(arg1,arg2,...)	#为myCamera提供的标定方法
    return Camera(arg1,arg2,...)
```

## 3 事件数据

### 3.1 事件数据对象创建或读取

事件数据支持**创建空对象、从已知相机的数据文件读取、从相机直接读取（通过相机驱动，见第5节）、从未知相机的数据文件读取（需要手动设定画幅）**

#### 3.1.1 空对象

```python
size=[y,x]
event=EventLab.Datas.getEmptyEvent(size)
```

#### 3.1.2 内建格式

##### 3.1.2.1 使用.txt文件

```python
direction=""	#.txt文件路径
xRow=1	#x坐标位于每一行的哪一列（默认为1）
yRow=2	#y坐标位于每一行的哪一列（默认为2）
timeStampRow=0	#时间戳位于每一行的哪一列（默认为0）
polarityRow=3	#极性位于每一行的哪一列（默认为3）
splitSymbol=" "	#每一行用于分割列的字符（默认为空格）
startStamp=0	#开始时间戳（默认为0）
endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）

event=camera.readEventFromText(direction,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#从已知相机的数据文件读取

size=[y,x]
event=EventLab.Datas.readEventFromText(size,direction,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#从未知相机的数据文件读取
```

##### 3.1.2.2  使用.mat文件

```python
direction=""	#.mat文件路径
field="event"	#指定字段（默认为该框架的默认.mat格式，即event字段下）
indexList=[]	#指定索引列表，由于.mat文件每个字段下是高维的数组结构，该列表指定了访问到储存事件数据的列优先二维数组所需要经过的索引（默认为该框架的默认.mat格式，即event字段下就是储存事件数据的列优先二维数组）
xRow=1	#x坐标位于储存事件数据的二维数组的哪一列（默认为1）
yRow=2	#y坐标位于储存事件数据的二维数组的哪一列（默认为2）
timeStampRow=0	#时间戳位于储存事件数据的二维数组的哪一列（默认为0）
polarityRow=3	#极性位于储存事件数据的二维数组的哪一列（默认为3）
startStamp=0	#开始时间戳（默认为0）
endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）

event=camera.readEventFromMat(direction,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#从已知相机的数据文件读取

size=[y,x]
event=EventLab.Datas.readEventFromMat(size,direction,field,indexList,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#从未知相机的数据文件读取
```

#### 3.1.3 自定义格式

```python
from EventLab.Objects.Event import Event

class EventFromMyFormat(Event)：
	def __init__(self,camera,size,arg1,arg2,...,startStamp,endStamp):
        super().__init__(camera,size)
        #在这里填写打开文件代码
        #循环开始
        	#读取一行数据的时间戳为ts
            if self._checkTimeStamp(ts,startStamp,endStamp):	#查询时间戳是否位于读取范围内
  				#读取一行数据的坐标x,坐标y,极性p
                self.addData(x,y,ts,p)
        #循环结束
        self.setData(array)	#不使用addData的话，也可以直接使用形状为[n,4]的numpy数组来设置数据（注意第一列为x坐标、第二列为y坐标、第三列为时间戳、第四列为极性）

#从未知相机的数据文件读取
def readEventFromMyFormat(size,arg1,arg2,...,startStamp,endStamp):
    return EventFromMyFormat(None,size,arg1,arg2,...,startStamp,endStamp)

#从已知相机的数据文件读取，参考2.3，并在实现中加入如下方法
def readEventFromMyFormat(self,arg1,arg2,...,startStamp,endStamp):
    return EventFromMyFormat(self.__Camera,None,arg1,arg2,...,startStamp,endStamp)
```

### 3.2 事件数据使用

```python
#读
event.readFromStartStamp()	#重置readData的迭代器，从第一条数据开始读取
data=[None,None,None,None]	#初始化用来接收event数据的列表
while(event.readData(data)):	#循环读取event直至结束
    #在这里对event数据进行处理
    #data[0]为event的x坐标
    #data[1]为event的y坐标
    #data[2]为event的时间戳
    #data[3]为event的极性

#写
eventResult=EventLab.Datas.getEmptyEvent(size)
eventResult.addData(x,y,ts,p)	#往空对象中添加一条数据
eventResult.setData(array)	#不使用addData的话，也可以直接使用形状为[n,4]的numpy数组来设置数据（注意第一列为x坐标、第二列为y坐标、第三列为时间戳、第四列为极性）

#其他
size=event.getSize()	#获取画幅
```

### 3.3 事件数据保存

#### 3.3.1 内建格式

##### 3.3.1.1 使用.txt文件

```python
direction=""	#目标.txt文件路径
EventLab.Datas.saveEventAsText(event,direction)	#保存结果
```

##### 3.3.1.2 保存为.mat文件

```python
direction=""	#目标.mat文件路径
EventLab.Datas.saveEventAsMat(event,direction)	#保存结果
```

#### 3.3.2 自定义格式

```python
from EventLab.Objects.EventSaver import EventSaver

class EventSaverToMyFormat(EventSaver):
    def save(self,arg1,arg2,...):
        #执行数据的读取与文件的写入，可以通过self._event来调用事件数据对象，使用方法参考3.2节“读”部分
```

## 4 帧数据

### 4.1 帧数据对象创建或读取

#### 4.1.1 空对象

```python
size=[y,x]
frames=EventLab.Datas.getEmptyFrame(size)
```

#### 4.1.2 内建格式

##### 4.1.2.1 使用.txt索引+图片目录

```python
directionOfIndex=""	#索引文件路径
directionOfImages=""	#储存外部图片的文件夹路径
stampRow=0	#时间戳位于每一行的哪一列（默认为0）
imgRow=1	#图片名位于每一行的哪一列（默认为不指定，这时框架会按顺序读取指定文件夹内的所有文件，请确定指定文件夹内文件按索引时间轴顺序排列完整且均为图片文件，以防报错）
splitSymbol=" "	#每一行用于分割列的字符（默认为空格）
startStamp=0	#开始时间戳（默认为0）
endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
startIndex=0	#开始的图片张数（默认不指定，同时指定开始的图片张数和开始时间戳时，以开始的图片张数优先）
endIndex=10	#结束的图片张数（默认不指定，同时指定结束的图片张数和结束时间戳时，以结束的图片张数优先）

frames=camera.readFrameByIndex(directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex,endIndex)	#从已知相机的数据文件读取

size=[y,x]
frames=EventLab.Datas.readFrameByIndex(size,directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex,endIndex)	#从未知相机的数据文件读取
```

##### 4.1.2.2 使用.mat文件

```python
direction=""	#.mat文件路径
field="APS"	#指定字段（默认为该框架的默认.mat格式，即APS字段下）
indexList=[]	#指定索引列表，由于.mat文件每个字段下是高维的数组结构，该列表指定了访问到储存APS数据的列优先二维数组所需要经过的索引（默认为该框架的默认.mat格式，即APS字段下就是储存APS数据的列优先二维数组）
timeStampRow=0	#时间戳位于储存APS数据的二维数组的哪一列（默认为0）
polarityRow=3	#图片位于储存APS数据的二维数组的哪一列（默认为1）
startStamp=0	#开始时间戳（默认为0）
endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
startIndex=0	#开始的图片张数（默认不指定，同时指定开始的图片张数和开始时间戳时，以开始的图片张数优先）
endIndex=10	#结束的图片张数（默认不指定，同时指定结束的图片张数和结束时间戳时，以结束的图片张数优先）

frames=camera.readFrameFromMat(direction,field,indexList,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#从已知相机的数据文件读取

size=[y,x]
frames=EventLab.Datas.readFrameFromMat(size,direction,field,indexList,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#从未知相机的数据文件读取
```

##### 4.1.2.3 使用视频流

```python
direction=""	#视频文件路径
startStamp=0	#开始时间戳（默认为0）
endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数，即视频末尾）
startIndex=0	#开始于第几帧（默认不指定，即从头开始）
endIndex=10	#结束于第几帧（默认不指定，即视频末尾）

frames=camera.readFrameFromVideo(direction,startStamp,endStamp,startIndex,endIndex)	#从已知相机的数据文件读取

size=[y,x]
frames=EventLab.Datas.readFrameFromVideo(direction,startStamp,endStamp,startIndex,endIndex)	#从未知相机的数据文件读取
```

#### 4.1.3 自定义格式

```python
from EventLab.Objects.Frame import Frame

class FrameFromMyFormat(Frame):
    def __init__(self,camera,size,arg1,arg2,...,startStamp,endStamp,startIndex,endIndex):
        super().__init__(camera,size)
        #在这里填写打开文件代码
        i=0
        #循环开始
        	#读取一条数据的时间戳为ts
            if self._checkTimeStampAndIndex(ts,startStamp,endStamp,i,startIndex,endIndex):	#查询时间戳和索引是否位于读取范围内
  				#读取一行数据的图片数组为img
                self.addData(ts,img)
            i+=1
        #循环结束
		self.setData(array)	#不使用addData的话，也可以直接使用形状为[n,2]的numpy数组来设置数据（注意第一列为时间戳、第二列为图片矩阵）

#从未知相机的数据文件读取
def readFrameFromMyFormat(size,arg1,arg2,...,startStamp,endStamp):
    return FrameFromMyFormat(None,size,arg1,arg2,...,startStamp,endStamp)

#从已知相机的数据文件读取，参考2.3，并在实现中加入如下方法
def readFrameFromMyFormat(self,arg1,arg2,...,startStamp,endStamp):
    return FrameFromMyFormat(self.__Camera,None,arg1,arg2,...,startStamp,endStamp)
```

### 4.2 帧数据使用

```python
#读
frames.readFromStartStamp()	#重置readData的迭代器，从第一条数据开始读取
data=[None,None]	#初始化用来接收event数据的列表
while(frames.readData(data)):	#循环读取event直至结束
    #在这里对frame数据进行处理
    #data[0]为frame的时间戳
    #data[1]为frame的图像矩阵
data=frames.readDataOnN(n)	#读取第n张frame数据
    
#写
frameResult=EventLab.Datas.getEmptyFrame(size)
frameResult.addData(ts,img)	#往空对象中添加一条数据
frameResult.setData(array)	#不使用addData的话，也可以直接使用形状为[n,2]的numpy数组来设置数据（注意第一列为时间戳、第二列为图片矩阵）
frameResult.addDataByDirection(ts,direction)	#直接从本地路径读取一张图片（画幅需要与数据对象画幅一致）

#其他
length=frames.getLength()	#获取帧数据数目
size=frames.getSize()	#获取画幅
```

### 4.3 帧数据保存

#### 4.3.1 内建格式

##### 4.3.1.1 保存单张图片

```python
direction=""	#保存路径
EventLab.Datas.saveOneFrame(frames,direction)	#仅将frames的第一张帧数据保存为direction所示的图片
```

##### 4.3.1.2 保存为索引+图片目录

```python
directionOfIndex=""	#索引文件路径
directionOfImages=""	#外部图片文件夹路径
instance.saveAPSAsIndex(directionOfIndex,directionOfImages)
```

##### 4.3.1.3 保存为.mat文件

```python
direction=""	#目标.mat文件路径
instance.saveAPSAsMat(direction)	#保存结果
```

##### 4.3.1.4 保存为视频流

```python
direction=""	#目标视频文件路径（默认.avi格式）
frameRate=30	#目标视频文件帧率
instance.saveAPSAsVideo(direction,frameRate)	#保存结果
```

#### 4.3.2 自定义格式

```python
from EventLab.Objects.FrameSaver import FrameSaver

class FrameSaverToMyFormat(FrameSaver):
    def save(self,arg1,arg2,...):
        #执行数据的读取与文件的写入，可以通过self._Frame来调用帧数据对象，使用方法参考4.2节“读”部分
```

## 5 从相机直接读取数据

### 5.1 inivation
请将项目Drives目录下的指定文件拷贝至工程目录

```python
direction="davis_simple.dylib"	#OSX
direction="davis_simple.so"	#linux

startStamp=0	#开始时间戳（默认为0）
endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）

event,frames=EventLab.EventCamera.DynamicInput(direction,startStamp,endStamp)
```

### 5.2 samsung

*待开发*

## 6 算法

### 6.1 处理算法

#### 6.1.1 自定义算法

```python
def myProcessAlgorithm(self,event,frames,...):	#在算法中传入需要的数据
    event.readFromStartStamp()
    frames.readFromStartStamp()
    #使用readData函数的场合，推荐先重置迭代器
    size=[y,x]
    eventResult=EventLab.Datas.getEmptyEvent(size)
    frameResult=EventLab.Datas.getEmptyFrame(size)
    #创建空对象用于保存结果
    
    #对数据进行处理，并保存结果
    return eventResult,frameResult
```

#### 6.1.2 内建算法

##### SAI

```python
frame=EventLab.Process.SAI(event,v,fre,fre_0,d,reference_time,lbd,thershold,c_on,c_off)	#使用非对称阈值法的事件流SAI
frame=EventLab.Process.SAINormal(frames,v,fre,fre_0,d,reference_time)	#使用均值法的普光图片序列SAI
```

##### 互补滤波器

```python
frame=EventLab.Process.ComplementaryFilterAlgorithm(event,frames,rebuildFrameRate,alpha1,pc,mc,L)
```

### 6.2 展示算法

#### 6.2.1 自定义算法

```python
def myDisplayAlgorithm(self,event,frames,...):	#在算法中传入需要的数据
    event.readFromStartStamp()
    frames.readFromStartStamp()
    #使用readData函数的场合，推荐先重置迭代器
    #对数据进行读取，并且使用各种方法展示（如matplotlib）
```

#### 6.2.2 内建算法

##### 事件点建帧

```python
EventLab.Display.BuildFrame(event,frames,exposureTime,showTime)	#将event和frames同步展示。每展示一张frames的数据，将其时间戳之后exposureTime（单位s）内的所有事件点按正红负蓝的方式建帧，并同步展示。每次展示showTime秒
EventLab.Display.BuildFrameWithTs(event,showTime,frameRate)	#从时间戳开始时刻开始，将每1/frameRate时间内的事件点按正红负蓝的方式建帧并展示。每次展示showTime秒
```

##### 3D点云

```python
EventLab.Display.cloudDisplay(event)
```

### 6.3 评估算法

#### 6.3.1 自定义算法

```python
from EventLab.Algorithm.EstimateAlgorithm import EstimateAlgorithm

class myEstimateClass(EstimateAlgorithm):
    def __init__(self):
        super().__init__()
        
	def _calculate(self,groundTruthImg,targetImg):
        #利用groundTruthImg和targetImg两个图像矩阵计算评估指标
        return measure	#measure为评估指标，为一个浮点数

def myEstimateAlgorithm(self,frames,groundTruth,bins=10):
    myEstimateClass().action(groundTruth,frames,bins)
```

* 基类自带action函数，会将groundTruth中每一张图片，与aps中**时间戳相同**的每一张图片**成对匹配**并代入_calculate函数计算得到评估结果，将评估结果保存
* 保存的评估结果会被统计其**均值E**与**方差D**，并以**频率分布直方图**的方式呈现
* 频率分布直方图的区间数目可以通过action函数的参数设定

#### 6.3.2 内建算法

##### SSIM

```python
EventLab.Estimate.getSSIM(frames,groundTruth,10)	#计算SSIM并在10个区间上显示频率分布直方图
```

##### PSNR

```python
EventLab.Estimate.getPSNR(frames,groundTruth,10)	#计算PSNR并在10个区间上显示频率分布直方图
```
