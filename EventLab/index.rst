.. toctree::
   :maxdepth: 3

   index.rst


1 EventLab包
============

EventCamera类是一个抽象的事件相机事务模型，通过对以下属性和方法进行集成，实现了一套\ **面向对象的事件相机相关应用开发平台**\ ：

1. **相机参数**\ （方法：相机\ **标定**\ ）

2. 源数据：\ **事件数据**\ 、\ **APS数据**\ （方法：数据的\ **读取**\ 和\ **展示**\ ）

3. 处理结果：\ **事件数据**\ 、\ **APS数据**\ （方法：\ **保存**\ 数据或直接\ **读取**\ 数据，数据的\ **展示**\ ）

4. 用于评估处理结果的\ **GroundTruth**\ （方法：\ **读取**\ ）

EventCamera类提供了如下一套完整的工作流：

**信号**\ （事件数据（与APS数据））——**变换系统**\ （用户开发算法）——>\ **信号**\ （事件数据（与APS数据））——**评估系统**\ （各种评估算法）——>\ **评估结果**\ （评估算法得出的指标）

其中，\ **所有方法均提供有可供用户自行开发的接口**

*目前框架架构\ *\ **仅考虑离线的IO方式**\ *\ ，后期计划添加基于ROS的在线IO支持。*

.. _header-n16:

1.1 调用默认的EventCamera类
---------------------------

.. code:: python

   from EventCamera import EventCamera

   instance=EventCamera()	#实例化相机模型

.. _header-n18:

1.2 使用自行拓展的EventCamera类
-------------------------------

在项目目录下新建文件，如myEventCamera.py，写入以下内容：

.. code:: python

   from EventCamera import EventCamera

   class myEventCamera(EventCamera):
       #在这里实现EventCamera的拓展接口函数

.. _header-n21:

2 相机标定
==========

.. _header-n22:

2.1 使用已经取得的内参矩阵
--------------------------

函数原型

.. code:: python

   def calibration(self,imgSize,K=[])

使用方法

.. code:: python

   K=[[fx,s,px],[0,fy,py],[0,0,1]]	#创建内参矩阵
   imgSize=(y,x)	#设定相机画幅
   instance.calibration(imgSize,K)
   instance.calibration(imgSize)	#无需考虑相机姿态的应用，可以不使用内参矩阵

.. _header-n27:

2.2 使用离线数据的张正友标定法
------------------------------

*待开发*

.. _header-n29:

2.3 使用自行开发的相机标定方法
------------------------------

在项目目录下新建文件，如myCamera.py，写入以下内容：

.. code:: python

   from Camera import Camera

   class myCamera(Camera):
       def __init__(self,arg1,arg2,...):
           #在该函数中对self._picSize=[None,None]（相机画幅）和self._K=[]（内参矩阵）进行更改

在myEventCamera.py中引入自行开发的Camera类：

.. code:: python

   from myCamera import myCamera

在myEventCamera.py中添加拓展接口函数：

.. code:: python

   def myCalibration(self,arg1,arg2,...):
       self._Camera=myCamera(arg1,arg2,...)

.. _header-n36:

3 事件源数据
============

.. _header-n37:

3.1 事件源数据读取
------------------

**请务必在完成相机标定后再进行事件源数据读取，并保证事件源数据坐标范围与标定时设置的相机画幅一致，否则将导致报错**

.. _header-n39:

3.1.1 使用.txt文件
~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readEventFromText(self,direction,xRow=1,yRow=2,timeStampRow=0,polarityRow=3,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff)

使用方法

.. code:: python

   direction=""	#.txt文件路径
   xRow=1	#x坐标位于每一行的哪一列（默认为1）
   yRow=2	#y坐标位于每一行的哪一列（默认为2）
   timeStampRow=0	#时间戳位于每一行的哪一列（默认为0）
   polarityRow=3	#极性位于每一行的哪一列（默认为3）
   splitSymbol=" "	#每一行用于分割列的字符（默认为空格）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   instance.readEventFromText(direction,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#进行数据读取

.. _header-n44:

3.1.2 使用.mat文件
~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readEventFromMat(self,direction,field="event",indexList=[],xRow=1,yRow=2,timeStampRow=0,polarityRow=3,startStamp=0,endStamp=0x7fffffff)

使用方法

.. code:: python

   direction=""	#.mat文件路径
   field="event"	#指定字段（默认为该框架的默认.mat格式，即event字段下）
   indexList=[]	#指定索引列表，由于.mat文件每个字段下是高维的数组结构，该列表指定了访问到储存事件数据的列优先二维数组所需要经过的索引（默认为该框架的默认.mat格式，即event字段下就是储存事件数据的列优先二维数组）
   xRow=1	#x坐标位于储存事件数据的二维数组的哪一列（默认为1）
   yRow=2	#y坐标位于储存事件数据的二维数组的哪一列（默认为2）
   timeStampRow=0	#时间戳位于储存事件数据的二维数组的哪一列（默认为0）
   polarityRow=3	#极性位于储存事件数据的二维数组的哪一列（默认为3）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   instance.readEventFromMat(direction,field,indexList,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#进行数据读取

.. _header-n49:

3.1.3 使用.bag文件
~~~~~~~~~~~~~~~~~~

*待开发*

.. _header-n51:

3.1.4 使用自行开发的数据读取算法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在项目目录下新建文件，如myEvent.py，写入以下内容：

.. code:: python

   from Event import Event

   class myEvent(Event):
       def __init__(self,camera,size,arg1,arg2,...,startStamp,endStamp):
           super().__init__(camera,size)
           #在这里填写打开文件代码
           #循环开始
           	#读取一行数据的时间戳为ts
               if self._checkTimeStamp(ts,startStamp,endStamp):	#查询时间戳是否位于读取范围内
     				#读取一行数据的坐标x,坐标y,极性p
                   self.addData(x,y,ts,p)
           #循环结束

在myEventCamera.py中引入自定义事件类：

.. code:: python

   from myEvent import myEvent

在myEventCamera.py中添加拓展接口函数：

.. code:: python

   def readEventFromMyFormat(self,arg1,arg2,...):
       self._Event=myEvent(self._Camera,None,arg1,arg2,...,startStamp,endStamp)

.. _header-n58:

3.2 事件源数据展示
------------------

事件源数据将以3D点云方式展示

函数原型

.. code:: python

   def sourceThreeDCloudShow(self)

使用方法

.. code:: python

   instance.sourceThreeDCloudShow()

展示示例

.. figure:: image-20200827111957498.png
   :alt: 

.. _header-n66:

4 APS源数据
===========

.. _header-n67:

4.1 APS源数据读取
-----------------

**请务必在完成相机标定后再进行APS源数据读取，并保证APS源数据图片尺寸与标定时设置的相机画幅一致，否则将导致报错**

.. _header-n69:

4.1.1 使用.txt索引+外部图片
~~~~~~~~~~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readAPSByIndex(self,directionOfIndex,directionOfImages,stampRow=0,imgRow=-1,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   directionOfIndex=""	#索引文件路径
   directionOfImages=""	#储存外部图片的文件夹路径
   stampRow=0	#时间戳位于每一行的哪一列（默认为0）
   imgRow=1	#图片名位于每一行的哪一列（默认为不指定，这时框架会按顺序读取指定文件夹内的所有文件，请确定指定文件夹内文件按索引时间轴顺序排列完整且均为图片文件，以防报错）
   splitSymbol=" "	#每一行用于分割列的字符（默认为空格）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   startIndex=0	#开始的图片张数（默认不指定，同时指定开始的图片张数和开始时间戳时，以开始的图片张数优先）
   endIndex=10	#结束的图片张数（默认不指定，同时指定结束的图片张数和结束时间戳时，以结束的图片张数优先）
   instance.readAPSByIndex(directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex,endIndex)	#进行数据读取

.. _header-n74:

4.1.2 使用.mat文件
~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readAPSFromMat(self,direction,field="APS",indexList=[],timeStampRow=0,imgRow=1,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   direction=""	#.mat文件路径
   field="APS"	#指定字段（默认为该框架的默认.mat格式，即APS字段下）
   indexList=[]	#指定索引列表，由于.mat文件每个字段下是高维的数组结构，该列表指定了访问到储存APS数据的列优先二维数组所需要经过的索引（默认为该框架的默认.mat格式，即APS字段下就是储存APS数据的列优先二维数组）
   timeStampRow=0	#时间戳位于储存APS数据的二维数组的哪一列（默认为0）
   polarityRow=3	#图片位于储存APS数据的二维数组的哪一列（默认为1）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   startIndex=0	#开始的图片张数（默认不指定，同时指定开始的图片张数和开始时间戳时，以开始的图片张数优先）
   endIndex=10	#结束的图片张数（默认不指定，同时指定结束的图片张数和结束时间戳时，以结束的图片张数优先）
   instance.readAPSFromMat(direction,field,indexList,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#进行数据读取

.. _header-n79:

4.1.3 使用.bag文件
~~~~~~~~~~~~~~~~~~

*待开发*

.. _header-n81:

4.1.4 使用视频流
~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readAPSFromVideo(self,direction,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   direction=""	#视频文件路径
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数，即视频末尾）
   startIndex=0	#开始于第几帧（默认不指定，即从头开始）
   endIndex=10	#结束于第几帧（默认不指定，即视频末尾）
   instance.readAPSFromVideo(direction,startStamp,endStamp,startIndex,endIndex)	#进行数据读取

.. _header-n86:

4.1.5 使用自行开发的数据读取算法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在项目目录下新建文件，如myAPS.py，写入以下内容：

.. code:: python

   from APS import APS

   class myAPS(APS):
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

在myEventCamera.py中引入自定义APS类：

.. code:: python

   from myAPS import myAPS

在myEventCamera.py中添加拓展接口函数：

.. code:: python

   def readAPSFromMyFormat(self,arg1,arg2,...):
       self._APS=myAPS(self._Camera,None,arg1,arg2,...,startStamp,endStamp,startIndex,endIndex)

.. _header-n93:

4.2 APS源数据展示
-----------------

每一张APS数据的生成均有曝光时间，在这段曝光时间中，产生的事件点将可以被建成事件帧，其中\ **红色事件点为正极性、蓝色事件点为负极性**\ 。

APS数据将以和对应的事件帧同步放映的方式展示。

函数原型

.. code:: python

   def sourceBuildFrameShow(self,exposureTime,showTime=0.05)

使用方法

.. code:: python

   exposureTime=0.06	#指定曝光时间（秒数）
   showTime=0.05	#指定放映停留时间（秒数，默认0.05s）
   instance.sourceBuildFrameShow(exposureTime,showTime)	#请务必在完成APS源数据和事件源数据的读取后使用，否则将导致报错

展示示例

.. _header-n102:

5 变换系统算法开发
==================

.. _header-n103:

5.1 使用Algorithm基类和AlgorithmWithAPS基类
-------------------------------------------

引入

.. code:: python

   from Algorithm import Algorithm
   from Algorithm import AlgorithmWithAPS

1. 所有的\ **使用event数据**\ 的算法，从\ **Algorithm类**\ 下派生

2. 所有的\ **使用event数据和APS数据**\ 的算法，从\ **AlgorithmWithAPS类**\ 下派生

.. code:: python

   class myAlgorithmClass(Algorithm):
   	def __init__(self,event,camera):
           super().__init__(event,camera)

   class myAlgorithmClassWithAPS(AlgorithmWithAPS)
       def __init__(self,event,aps,camera):
           super().__init__(event,aps,camera)

-  Algorithm基类和AlgorithmWithAPS基类构造函数会\ **自动检查相机是否标定、各项数据是否初始化**

-  Algorithm基类和AlgorithmWithAPS基类构造函数会自动设置event数据和APS数据（若有）\ **从第一条数据开始读取**

.. _header-n117:

5.2 编制action函数
------------------

请在派生的算法类中，实现核心action函数

.. code:: python

   def action(self,arg1,arg2,...):
       #在这里编写算法，“arg1,arg2,...”为算法参数

算法实现中用到的变量命名，请尽量使用\ **完整拼写的英文短语**\ ，并尽量遵守\ **小驼峰法**

小驼峰法示例：

sampleOfIt

.. _header-n123:

5.3 在自定义EventCamera类中实现函数接口
---------------------------------------

1. 在myEventCamera.py中引入自定义算法类

2. 在myEventCamera类中添加函数接口

.. code:: python

   def myAlgorithmInterface(self,arg1,arg2,...):
       myAlgorithmClass.(self._Event,self._Camera).action(arg1,arg2,...)
   #无返回结果

   def myAlgorithmInterfaceWithAPS(self,arg1,arg2,...):
       myAlgorithmClassWithAPS.(self._Event,self._APS,self._Camera).action(arg1,arg2,...)
   #无返回结果

   def myAlgorithmInterfaceWithAPS(self,arg1,arg2,...):
       self._EventResult=myAlgorithmClassWithAPS.(self._Event,self._APS,self._Camera).action(arg1,arg2,...)
   #返回事件流
       
   def myAlgorithmInterfaceWithAPS(self,arg1,arg2,...):
       self._APSResult=myAlgorithmClassWithAPS.(self._Event,self._APS,self._Camera).action(arg1,arg2,...)
   #返回APS数据

这样，外界若想要调用新增的算法，只需通过函数接口即可

.. code:: python

   instance.myAlgorithmInterface(arg1,arg2,...)
   instance.myAlgorithmInterfaceWithAPS(arg1,arg2,...)

.. _header-n132:

5.4 使用数据
------------

.. _header-n133:

5.4.1 使用相机参数
~~~~~~~~~~~~~~~~~~

+-------------------+-----------------------+-----------------------+
| 作用              | 示例                  | 返回值说明            |
+===================+=======================+=======================+
| 获取画幅          | size=s                | size=(y,x)            |
|                   | elf._Camera.getSize() |                       |
+-------------------+-----------------------+-----------------------+
| 获取内参矩阵      | K=self._Camera.getK() | K=[[fx,s,p            |
|                   |                       | x],[0,fy,py],[0,0,1]] |
+-------------------+-----------------------+-----------------------+
| 获取x方向焦距     | fx                    |                       |
|                   | =self._Camera.getFx() |                       |
+-------------------+-----------------------+-----------------------+
| 获取y方向焦距     | fy                    |                       |
|                   | =self._Camera.getFy() |                       |
+-------------------+-----------------------+-----------------------+
| 获取畸变系数      | s=self._Camera.getS() |                       |
+-------------------+-----------------------+-----------------------+
| 获取x方向主轴偏移 | px                    |                       |
|                   | =self._Camera.getPx() |                       |
+-------------------+-----------------------+-----------------------+
| 获取y方向主轴偏移 | py                    |                       |
|                   | =self._Camera.getPy() |                       |
+-------------------+-----------------------+-----------------------+

.. _header-n167:

5.4.2 使用事件源数据
~~~~~~~~~~~~~~~~~~~~

.. _header-n168:

readData
^^^^^^^^

函数原型

.. code:: python

   def readData(self,event)

使用示例

.. code:: python

   event=[0,0,0,0]	#初始化用来接收event数据的列表
   while(self._Event.readData(event)):	#循环读取event直至结束
       #在这里对event数据进行处理
       #event[0]为event的x坐标
       #event[1]为event的y坐标
       #event[2]为event的时间戳
       #event[3]为event的极性

.. _header-n173:

readFromStartStamp
^^^^^^^^^^^^^^^^^^

函数原型

.. code:: python

   def readFromStartStamp(self)

使用示例

.. code:: python

   self._Event.readFromStartStamp()	#从第一条数据开始读取

.. _header-n178:

5.4.3 使用APS源数据
~~~~~~~~~~~~~~~~~~~

.. _header-n179:

readData
^^^^^^^^

函数原型

.. code:: python

   def readData(self,data)

使用示例

.. code:: python

   data=[0,0]	#初始化用来接收APS数据的列表
   while(self._APS.readData(data)):	#循环读取APS数据直至结束
       #在这里对APS数据进行处理
       #data[0]为APS数据的时间戳
       #data[1]为APS数据的图像本身，以二维numpy.ndarray方式储存

.. _header-n184:

readDataOnN
^^^^^^^^^^^

函数原型

.. code:: python

   def readDataOnN(self,n)

使用示例

.. code:: python

   n=10	#指定需要读取第几张图片
   timestamp,img=self._APS.readDataOnN(n)	#获取第n张图片的时间戳与图片本身，图片本身以二维numpy.ndarray方式储存

.. _header-n189:

readFromStartStamp
^^^^^^^^^^^^^^^^^^

函数原型

.. code:: python

   def readFromStartStamp(self)

使用示例

.. code:: python

   self._APS.readFromStartStamp()	#从第一条数据开始读取

.. _header-n194:

5.5 输出结果事件流
------------------

.. _header-n195:

5.5.1 在算法类中新建结果事件流
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from Event import Event

   eventResult=Event(self._Camera,None)

.. _header-n197:

5.5.2 addData
~~~~~~~~~~~~~

.. code:: python

   eventResult.addData(x,y,ts,p)	#增加一条数据，x和y为坐标，ts为时间戳，p为极性

.. _header-n199:

5.5.3 返回结果事件流
~~~~~~~~~~~~~~~~~~~~

action函数的最后返回：

.. code:: python

   return eventResult

.. _header-n202:

5.6 输出结果APS数据
-------------------

.. _header-n203:

5.6.1 在算法类中新建结果APS数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from APS import APs

   APSResult=APS(self._Camera,None)

.. _header-n205:

5.6.2 addData
~~~~~~~~~~~~~

.. code:: python

   eventResult.addData(ts,img)	#增加一条数据，ts为时间戳，img为图片数组

.. _header-n207:

5.6.3 返回结果APS数据
~~~~~~~~~~~~~~~~~~~~~

action函数的最后返回：

.. code:: python

   return APSResult

.. _header-n210:

5.7 变换算法一览
----------------

*请在该栏目添加利用该框架开发的算法及其原型*

.. _header-n212:

6 处理结果
==========

.. _header-n213:

6.1 保存事件处理结果
--------------------

.. _header-n214:

6.1.1 保存为.txt文件
~~~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def saveEventAsText(self,direction)

使用方法

.. code:: python

   direction=""	#目标.txt文件路径
   instance.saveEventAsText(direction)	#保存结果

将以“x y ts
p”的格式，按每行一条事件进行储存。其中x和y为坐标，ts为时间戳，p为事件极性

.. _header-n220:

6.1.2 保存为.mat文件
~~~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def saveEventAsMat(self,direction)

使用方法

.. code:: python

   direction=""	#目标.mat文件路径
   instance.saveEventAsMat(direction)	#保存结果

将event数据储存在目标.mat文件的"event"字段下，按列优先方式存储。其中，每条事件的x坐标位于第一列、y坐标位于第二列、时间戳位于第三列、事件极性位于第四列

.. _header-n226:

6.1.3 保存为.bag文件
~~~~~~~~~~~~~~~~~~~~

*待开发*

.. _header-n228:

6.1.4 保存为自定义格式
~~~~~~~~~~~~~~~~~~~~~~

在项目目录下新建文件，如myEventSaver.py，写入以下内容：

.. code:: python

   from EventSaver import EventSaver

   class myEventSaver(EventSaver):
       def save(self,direction):
           #执行direction下文件的写入，可以通过self._event来调用事件处理结果，使用方法参考5.4.2节

在myEventCamera.py中引入自定义Event保存器类：

.. code:: python

   from myEventSaver import myEventSaver

在myEventCamera.py中添加拓展接口函数：

.. code:: python

   def saveEventAsMyFormat(self,direction):
       myEventSaver(self._EventResult).save(direction)

.. _header-n235:

6.2 保存APS数据处理结果
-----------------------

.. _header-n236:

6.2.1 保存为.txt索引+外部图片
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def saveAPSAsIndex(self,directionOfIndex,directionOfImages)

使用方法

.. code:: python

   directionOfIndex=""	#索引文件路径
   directionOfImages=""	#外部图片文件夹路径
   instance.saveAPSAsIndex(directionOfIndex,directionOfImages)

将图片索引按“ts
name”方式存储于索引文件中，每一张图片对应一行。其中ts为时间戳，name为图片名

.. _header-n242:

6.2.2 保存为.mat文件
~~~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def saveAPSAsMat(self,direction)

使用方法

.. code:: python

   direction=""	#目标.mat文件路径
   instance.saveAPSAsMat(direction)	#保存结果

将APS数据储存在目标.mat文件的"APS"字段下，按列优先方式存储。其中，每张图片的时间戳位于第一列、图片本身位于第二列

.. _header-n248:

6.2.3 保存为视频流
~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def saveAPSAsVideo(self,direction,frameRate)

使用方法

.. code:: python

   direction=""	#目标视频文件路径（默认.avi格式）
   frameRate=30	#目标视频文件帧率
   instance.saveAPSAsVideo(direction,frameRate)	#保存结果

.. _header-n253:

6.2.4 保存为.bag文件
~~~~~~~~~~~~~~~~~~~~

*待开发*

.. _header-n255:

6.2.5 保存为自定义格式
~~~~~~~~~~~~~~~~~~~~~~

在项目目录下新建文件，如myAPSSaver.py，写入以下内容：

.. code:: python

   from APSSaver import APSSaver

   class myAPSSaver(APSSaver):
       def save(self,direction):
           #执行direction下文件的写入，可以通过self._APS来调用事件处理结果，使用方法参考5.4.3节

在myEventCamera.py中引入自定义Event保存器类：

.. code:: python

   from myAPSSaver import myAPSSaver

在myEventCamera.py中添加拓展接口函数：

.. code:: python

   def saveAPSAsMyFormat(self,direction):
       myAPSSaver(self._APSResult).save(direction)

.. _header-n262:

6.3 事件流处理结果读取
----------------------

可以直接读取外部已有处理结果，以进行展示或使用评估算法

.. _header-n264:

6.3.1 使用.txt文件
~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readEventResultFromText(self,direction,xRow=1,yRow=2,timeStampRow=0,polarityRow=3,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff)

使用方法

.. code:: python

   direction=""	#.txt文件路径
   xRow=1	#x坐标位于每一行的哪一列（默认为1）
   yRow=2	#y坐标位于每一行的哪一列（默认为2）
   timeStampRow=0	#时间戳位于每一行的哪一列（默认为0）
   polarityRow=3	#极性位于每一行的哪一列（默认为3）
   splitSymbol=" "	#每一行用于分割列的字符（默认为空格）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   instance.readEventResultFromText(direction,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#进行数据读取

.. _header-n269:

6.3.2 使用.mat文件
~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readEventResultFromMat(self,direction,field="event",indexList=[],xRow=1,yRow=2,timeStampRow=0,polarityRow=3,startStamp=0,endStamp=0x7fffffff)

使用方法

.. code:: python

   direction=""	#.mat文件路径
   field="event"	#指定字段（默认为该框架的默认.mat格式，即event字段下）
   indexList=[]	#指定索引列表，由于.mat文件每个字段下是高维的数组结构，该列表指定了访问到储存事件数据的列优先二维数组所需要经过的索引（默认为该框架的默认.mat格式，即event字段下就是储存事件数据的列优先二维数组）
   xRow=1	#x坐标位于储存事件数据的二维数组的哪一列（默认为1）
   yRow=2	#y坐标位于储存事件数据的二维数组的哪一列（默认为2）
   timeStampRow=0	#时间戳位于储存事件数据的二维数组的哪一列（默认为0）
   polarityRow=3	#极性位于储存事件数据的二维数组的哪一列（默认为3）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   instance.readEventResultFromMat(direction,field,indexList,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#进行数据读取

.. _header-n274:

6.3.3 使用.bag文件
~~~~~~~~~~~~~~~~~~

*待开发*

.. _header-n276:

6.3.4 使用自行开发的数据读取算法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

参考3.1.4节

在myEventCamera.py中添加拓展接口函数：

.. code:: python

   def readEventResultFromMyFormat(self,size,arg1,arg2,...):
       self._Event=myEvent(None,size,arg1,arg2,...,startStamp,endStamp)

.. _header-n280:

6.4 APS数据处理结果读取
-----------------------

可以直接读取外部已有处理结果，以进行展示或使用评估算法

.. _header-n282:

6.4.1 使用.txt索引+外部图片
~~~~~~~~~~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readAPSResultByIndex(self,directionOfIndex,directionOfImages,stampRow=0,imgRow=-1,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   directionOfIndex=""	#索引文件路径
   directionOfImages=""	#储存外部图片的文件夹路径
   stampRow=0	#时间戳位于每一行的哪一列（默认为0）
   imgRow=1	#图片名位于每一行的哪一列（默认为不指定，这时框架会按顺序读取指定文件夹内的所有文件，请确定指定文件夹内文件按索引时间轴顺序排列完整且均为图片文件，以防报错）
   splitSymbol=" "	#每一行用于分割列的字符（默认为空格）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   startIndex=0	#开始的图片张数（默认不指定，同时指定开始的图片张数和开始时间戳时，以开始的图片张数优先）
   endIndex=10	#结束的图片张数（默认不指定，同时指定结束的图片张数和结束时间戳时，以结束的图片张数优先）
   instance.readAPSResultByIndex(directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex,endIndex)	#进行数据读取

.. _header-n287:

6.4.2 使用.mat文件
~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readAPSFromMat(self,direction,field="APS",indexList=[],timeStampRow=0,imgRow=1,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   direction=""	#.mat文件路径
   field="APS"	#指定字段（默认为该框架的默认.mat格式，即APS字段下）
   indexList=[]	#指定索引列表，由于.mat文件每个字段下是高维的数组结构，该列表指定了访问到储存APS数据的列优先二维数组所需要经过的索引（默认为该框架的默认.mat格式，即APS字段下就是储存APS数据的列优先二维数组）
   timeStampRow=0	#时间戳位于储存APS数据的二维数组的哪一列（默认为0）
   polarityRow=3	#图片位于储存APS数据的二维数组的哪一列（默认为1）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   startIndex=0	#开始的图片张数（默认不指定，同时指定开始的图片张数和开始时间戳时，以开始的图片张数优先）
   endIndex=10	#结束的图片张数（默认不指定，同时指定结束的图片张数和结束时间戳时，以结束的图片张数优先）
   instance.readAPSResultFromMat(direction,field,indexList,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#进行数据读取

.. _header-n292:

6.4.3 使用.bag文件
~~~~~~~~~~~~~~~~~~

*待开发*

.. _header-n294:

6.4.4 使用视频流
~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readAPSResultFromVideo(self,direction,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   direction=""	#视频文件路径
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数，即视频末尾）
   startIndex=0	#开始于第几帧（默认不指定，即从头开始）
   endIndex=10	#结束于第几帧（默认不指定，即视频末尾）
   instance.readAPSResultFromVideo(direction,startStamp,endStamp,startIndex,endIndex)	#进行数据读取

.. _header-n299:

6.4.5 使用自行开发的数据读取算法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

参考4.1.5节

在myEventCamera.py中添加拓展接口函数：

.. code:: python

   def readAPSResultFromMyFormat(self,size,arg1,arg2,...):
       self._APS=myAPS(None,size,arg1,arg2,...,startStamp,endStamp,startIndex,endIndex)

.. _header-n303:

6.5 事件流处理结果展示
----------------------

函数原型

.. code:: python

   def resultThreeDCloudShow(self)

使用方法

.. code:: python

   instance.resultThreeDCloudShow()

展示效果参考3.2节

.. _header-n309:

6.6 APS处理结果展示
-------------------

同时存在事件流处理结果与APS处理结果时方可调用

函数原型

.. code:: python

   def resultBuildFrameShow(self,exposureTime,showTime=0.05)

使用方法

.. code:: python

   exposureTime=0.06	#指定曝光时间（秒数）
   showTime=0.05	#指定放映停留时间（秒数，默认0.05s）
   instance.resultBuildFrameShow(exposureTime,showTime)

展示效果参考4.2节

.. _header-n316:

7 评估系统算法开发
==================

*目前仅提供基于APS数据和APS Ground Truth的评估算法*

.. _header-n318:

7.1 读取GroundTruth
-------------------

.. _header-n319:

7.1.1 使用.txt索引+外部图片
~~~~~~~~~~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readGroundTruthByIndex(self,directionOfIndex,directionOfImages,stampRow=0,imgRow=-1,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   directionOfIndex=""	#索引文件路径
   directionOfImages=""	#储存外部图片的文件夹路径
   stampRow=0	#时间戳位于每一行的哪一列（默认为0）
   imgRow=1	#图片名位于每一行的哪一列（默认为不指定，这时框架会按顺序读取指定文件夹内的所有文件，请确定指定文件夹内文件按索引时间轴顺序排列完整且均为图片文件，以防报错）
   splitSymbol=" "	#每一行用于分割列的字符（默认为空格）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   startIndex=0	#开始的图片张数（默认不指定，同时指定开始的图片张数和开始时间戳时，以开始的图片张数优先）
   endIndex=10	#结束的图片张数（默认不指定，同时指定结束的图片张数和结束时间戳时，以结束的图片张数优先）
   instance.readGroundTruthByIndex(directionOfIndex,directionOfImages,stampRow,imgRow,splitSymbol=" ",startStamp=0,endStamp=0x7fffffff,startIndex,endIndex)	#进行数据读取

.. _header-n324:

7.1.2 使用.mat文件
~~~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readGroundTruthFromMat(self,direction,field="APS",indexList=[],timeStampRow=0,imgRow=1,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   direction=""	#.mat文件路径
   field="APS"	#指定字段（默认为该框架的默认.mat格式，即APS字段下）
   indexList=[]	#指定索引列表，由于.mat文件每个字段下是高维的数组结构，该列表指定了访问到储存APS数据的列优先二维数组所需要经过的索引（默认为该框架的默认.mat格式，即APS字段下就是储存APS数据的列优先二维数组）
   timeStampRow=0	#时间戳位于储存APS数据的二维数组的哪一列（默认为0）
   polarityRow=3	#图片位于储存APS数据的二维数组的哪一列（默认为1）
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数）
   startIndex=0	#开始的图片张数（默认不指定，同时指定开始的图片张数和开始时间戳时，以开始的图片张数优先）
   endIndex=10	#结束的图片张数（默认不指定，同时指定结束的图片张数和结束时间戳时，以结束的图片张数优先）
   instance.readGroundTruthFromMat(direction,field,indexList,xRow,yRow,timeStampRow,polarityRow,startStamp,endStamp)	#进行数据读取

.. _header-n329:

7.1.3 使用.bag文件
~~~~~~~~~~~~~~~~~~

*待开发*

.. _header-n331:

7.1.4 使用视频流
~~~~~~~~~~~~~~~~

函数原型

.. code:: python

   def readGroundTruthFromVideo(self,direction,startStamp=0,endStamp=0x7fffffff,startIndex=-1,endIndex=-1)

使用方法

.. code:: python

   direction=""	#视频文件路径
   startStamp=0	#开始时间戳（默认为0）
   endStamp=0x7fffffff	#结束时间戳（默认为64位最大浮点数，即视频末尾）
   startIndex=0	#开始于第几帧（默认不指定，即从头开始）
   endIndex=10	#结束于第几帧（默认不指定，即视频末尾）
   instance.readGroundTruthFromVideo(direction,startStamp,endStamp,startIndex,endIndex)	#进行数据读取

.. _header-n336:

7.1.5 使用自行开发的数据读取算法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

参考4.1.5节

在myEventCamera.py中添加拓展接口函数：

.. code:: python

   def readGroundTruthFromMyFormat(self,size,arg1,arg2,...):
       self._GroundTruth=myAPS(None,size,arg1,arg2,...,startStamp,endStamp,startIndex,endIndex)

.. _header-n340:

7.2 使用EstimateAlgorithm基类
-----------------------------

引入

.. code:: python

   from Estimate import EstimateAlgorithm

所有的评估的算法，从EstimateAlgorithm下派生：

.. code:: python

   class myEstimateClass(EstimateAlgorithm):
   	def __init__(self,aps,groundTruth):
           super().__init__(aps,groundTruth)

-  基类构造函数会\ **自动检查相机是否标定、各项数据是否初始化**

.. _header-n348:

7.3 编制_calculate函数
----------------------

.. code:: python

   def _calculate(self,groundTruthImg,apsImg):
       #利用groundTruthImg和apsImg两个二维ndarray计算评估指标
       return measure	#measure为评估指标，为一个浮点数

.. _header-n350:

7.4 评估结果统计与展示
----------------------

-  基类自带action函数，会将groundTruth中每一张图片，与aps中\ **时间戳相同**\ 的每一张图片\ **成对匹配**\ 并带入_calculate函数计算得到评估结果，将评估结果保存

-  保存的评估结果会被统计其\ **均值E**\ 与\ **方差D**\ ，并以\ **频率分布直方图**\ 的方式呈现

-  频率分布直方图的区间数目可以通过action函数的参数设定

展示效果：

.. _header-n360:

7.5 在自定义EventCamera类中实现函数接口
---------------------------------------

1. 在myEventCamera.py中引入自定义评估算法类

2. 在myEventCamera类中添加函数接口

.. code:: python

   def myEstimateInterface(self,bins):
       myEstimateClass.(self._APS,self._GroundTruth).action(bins)	#bins为频率分布直方图的区间数目

这样，外界若想要调用新增的评估算法，只需通过函数接口即可

.. code:: python

   instance.myEstimateInterface(arg1,arg2,...)

.. _header-n369:

7.6 评估算法一览
----------------

*请在该栏目添加利用该框架开发的评估算法及其原型*

.. _header-n371:

SSIM
~~~~

函数原型

.. code:: python

   def getSSIM(self,bins=10)

使用方法

.. code:: python

   instance.getSSIM(10)	#计算SSIM并在10个区间上显示频率分布直方图

.. _header-n376:

PSNR
~~~~

函数原型

.. code:: python

   def getPSNR(self,bins=10)

使用方法

.. code:: python

   instance.getPSNR(10)	#计算SSIM并在10个区间上显示频率分布直方图

.. _header-n381:

FSIM
~~~~

*待开发*
