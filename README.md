# script_arknight
## 1.简介
  自己写的针对windows模拟器的游戏脚本，这个是自己平时为了偷懒写的，代码上仍有很多进步空间，由于近期事情较多，界面和打包都先挖个坑，后期有时间再说。现在能自动肝活动本，节约了不少时间。

明日方舟调用库：
PIL，pywin32，opencv
少女前线调用库：
多一个pyocr



## 2.基本原理说明：
  利用抓取windows窗口图像，并对图像进行基本识别操作后对模拟器窗口发送虚拟操作指令，由于是在模拟器之外的，因此原理上不会有风险。
缺点是模拟器无法最小化，因windows程序最小化停止重绘窗口，无法抓取到窗体图像。

## 3.脚本功能（针对2019-5-30版本）
  1.活动图GT2-6可以选择  
  2.理智不足可以碎石    （config_ark.py 配置）  
  3.脚本开始位置无要求，可以从不同界面，或者是战斗中等开始脚本  
  4.自适应分辨率，最高支持1080p， 目前测试了720p没有问题  
  5.支持夜神模拟器

## 4.有空完成的功能：
  1.gui  
  2.打包  
  3.自动每日主线任务  
  4.自动基建干员分配  
