#self.installPlugin3Btn.clicked.connect(MainWindow.InstallPluginFun3)  # type: ignore


from PyQt5 import QtCore, QtGui, QtWidgets
from hdqt5ui import *
from HD import *
import datetime
import time
import sys

g_全局窗口序号 = 1
g_全局PID = 0 #可以为0,但是必须指定打开回调,打开回调返回PID
g_全局接口类型 = 3 # 3 5 7
g_全局窗口句柄 = 0
#第四节课 HD安装插件方式一
#打开回调 打开进程 新的进程 会产生一个新PID
# HD安装_打开回调
# typedef __int64(__stdcall *UIFUNTYPE)(__int32 窗口序号);
@HD_OpenFunType_stdcall #注意要用类型申明下
def 打开回调3(窗口序号):#对于方式一的打开回调的返回值: 大于0 表示成功同时还表示窗口句柄 小于等于0失败(中断HD扩展_安装插件3 并把这个返回值返回)
    #打开进程的逻辑...
    #...
    print(f"open_callBack2 winIndex:{窗口序号}")
    ret =  HD系统_启动EXE带参数Ex("D:\XTLBB\Bin64","Game.exe","-fl",0,0)#成功 返回PID  失败 返回小于0的值
    if ret <= 0:
        return ret

    #成功打开 ret == PID
    timeout = datetime.timedelta(seconds=30)  # 设置超时为30秒
    start_time = datetime.datetime.now()
    while True:
        # 执行其他操作（如检查文件、API响应等）
        current_time = datetime.datetime.now()
        #每一秒检查一下 窗口句柄是否出现
        findRet = HD窗口_枚举查找窗口Ex(ret,"TianLongBaBu WndClass","",26,False)
        print(f"是否窗口句柄{findRet}")
        if findRet == 1:
            #所有没有指定窗口序号的接口 需要拿到缓冲区或者字符串信息或者JSON字符串
            #需要通过
            #窗口序号怎么指定? 以【HD通用_获取最近返回Json】最近的上一个HD接口为准
            # 没有指定窗口序号就指定为0 表示从中控环境中拿信息
            # 如果指定了 就以指定的窗口序号为准
            hwnd =  int(HD通用_获取最近返回Json(0))#"0x456" 0x456
            print(f"拿到窗口句柄{hwnd}")
            global g_全局窗口句柄
            g_全局窗口句柄 = hwnd
            return hwnd
        if current_time - start_time > timeout:
            print("操作超时！")
            return HD返回值.ERROR_超时返回
        time.sleep(1)  # 避免CPU满载
    return -1

#检查回调 检查一些参数 重连窗口进程
# typedef __int64(__stdcall *UIFUNTYPE)(int 窗口序号, int 之前窗口序号, int 之前进程PID, int 提示值);
@HD_CHFunType_stdcall #注意要用类型申明下
def 检查回调(窗口序号,之前窗口序号,之前窗口PID,提示值):
    #检查进程的逻辑...
    print(f"check_CallBack2 winIndex:{窗口序号},preWinIndex:{之前窗口序号},prePid:{之前窗口PID},error:{提示值}")
    if 提示值 == HD返回值.RET_重连窗口:# 窗口序号==之前窗口序号 窗口序号
        # 5
        # 之前(g_全局窗口序号) 绑定的进程 还存在- 内部检查到- 告诉开发者可以重连 -至于是否重连 -开发者来控制
        return 1 # 同意重连
        # 如果 开发者不想重连 这个时间
        # 特殊需求
        # 终止 之前窗口PID 进行
        return 0 # 触发打开回调 新窗口

    if 提示值 == HD返回值.RET_重连窗口序号不一致: # 之前窗口序号 窗口序号/错误值
        # 6
        # 之前(g_全局窗口序号) 绑定过进程 -内部发现进程不存在 - 不存在的返回值 赋值给 {之前窗口序号} -触发检查回调
        if 之前窗口序号 == HD返回值.ERROR_进程不存在:
            return 0 # 触发打开回调 新窗口
        if 之前窗口序号 == HD返回值.ERROR_未安装插件:
            return 0 # 触发打开回调 新窗口
        if 之前窗口序号 > 0:
            #之前窗口序号 含义:窗口序号
            # 终止 之前窗口PID 进行
            return 0  # 触发打开回调 新窗口
    return -2# 返回小于0的值  自定义的或者是HD自带的错误值  中断安装流程 并返回




class HDUi_MainWindow(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)#调用父类的setupUi
        #在这下面可以 设置一些回调函数 信号槽
        self.installPlugin3Btn.clicked.connect(self.InstallPluginFun3)
        self.startCaptureBtn.clicked.connect(self.StartCaptureFun)
        self.closeCaptureBtn.clicked.connect(self.CloseCaptureFun)
        self.bindBtn.clicked.connect(self.BindFun)
        self.pauseBindBtn.clicked.connect(self.PauseBindFun)
        self.recoverBindBtn.clicked.connect(self.RecoverBindFun)
        self.unbindBtn.clicked.connect(self.UnBindFun)
        self.findPicBtn.clicked.connect(self.FindPicFun)
        self.findWordBtn.clicked.connect(self.FindWordFun)
    def InstallPluginFun3(self):
        print("InstallPluginFun3")
        # 打开新的
        global g_全局PID
        global g_全局窗口句柄
        g_全局PID = HD扩展_安装插件3(g_全局窗口序号, g_全局接口类型, g_全局窗口句柄, 64, 0, 0, 打开回调3, 检查回调, 30000)
        # 重新捕捉一下句柄
        if g_全局PID >0 :
            findRet = HD窗口_枚举查找窗口Ex(g_全局PID, "TianLongBaBu WndClass", "", 26, False)
            print(f"是否窗口句柄{findRet}")
        if findRet == 1:
            g_全局窗口句柄 = int(HD通用_获取最近返回Json(0))  # "0x456" 0x456
            print(f"捕捉拿到窗口句柄{g_全局窗口句柄}")
        # 赋值全局句柄
        print(f"第一次安装(进程不存在的情况){g_全局PID},{g_全局窗口句柄}")  # 大于0 PID 小于等于0 错误值

    def StartCaptureFun(self):
        print(f"StartCaptureFun{g_全局窗口句柄}")
        ret = HD截图_打开Ex(g_全局窗口序号,True,10,g_全局窗口句柄)
        print(f"HD截图_打开Ex:{g_全局PID},{g_全局窗口句柄}")  # 大于0 成功 小于等于0失败

    def CloseCaptureFun(self):
        print("StartCaptureFun")
        ret = HD截图_关闭Ex(g_全局窗口序号)
        print(f"HD截图_关闭Ex:{ret}")  # 大于0 成功 小于等于0失败

    def BindFun(self):
        print("BindFun")
        ret = HD键鼠_模式绑定Ex(g_全局窗口序号,g_全局窗口句柄,"1|0|1|1|1|1|1|0|0|0|1|1|1|0|1|0|0|0|0|0|",1)
        print(f"HD键鼠_模式绑定Ex:{ret},{g_全局窗口句柄}")  # 大于0 成功 小于等于0失败

    def UnBindFun(self):
        print("UnBindFun")
        ret = HD键鼠_解绑(g_全局窗口序号)
        print(f"HD键鼠_解绑:{ret}")  # 大于0 成功 小于等于0失败

    def PauseBindFun(self):
        print("PauseBindFun")
        ret = HD键鼠_暂停绑定(g_全局窗口序号,True,1)
        print(f"HD键鼠_暂停绑定:{ret}")  # 大于0 成功 小于等于0失败

    def RecoverBindFun(self):
        print("RecoverBindFun")
        ret = HD键鼠_暂停绑定(g_全局窗口序号,False,1)
        print(f"HD键鼠_恢复绑定:{ret}")  # 大于0 成功 小于等于0失败

    def FindPicFun(self):
         print("FindPicFun")
         ret = HD识图_范围找图Ex(g_全局窗口序号,-1,-1,-1,-1,"Pic40.bmp|Pic40.bmp|Pic40.bmp","303030",0.9,0)
         jsonStr = HD通用_获取最近返回Json(g_全局窗口序号)
         print(f"json:{jsonStr}")
         print(f"HD识图_范围找图Ex:{ret}")  # 大于0 成功 小于等于0失败

    def FindPicTemFun(self):
         print("FindPicTemFun")
         ret = HD智能识图_Tem找图A(g_全局窗口序号,"Pic41.bmp",0.9,3,True,False,False)
         jsonStr = HD通用_获取最近返回Json(g_全局窗口序号)
         print(f"json:{jsonStr}")
         print(f"HD智能识图_Tem找图A:{ret}")  # 大于0 成功 小于等于0失败

    def FindWordFun(self):
        print("FindWordFun")
        #759,522,1083,695|(324,173)
        ret = HD识字_设置字库(g_全局窗口序号, 10 , "HD_Dict.txt")#默认使用的是第一个加的字库文件
        ret = HD识字_设置字库(g_全局窗口序号, 2 , "HD_Dict.txt")#如果要用这个 就需要切换字库序号
        ret = HD识字_设置字库(g_全局窗口序号, 3, "HD_Dict.txt")
        ret = HD识字_设置字库(g_全局窗口序号, 4, "HD_Dict.txt")
        print(f"HD识字_设置字库:{ret}")
        ret = HD识字_获取当前字库序号(g_全局窗口序号)#看一看默认的序号？
        print(f"切换前 HD识字_获取当前字库序号:{ret}")

        ret = HD识字_获取当前字库(g_全局窗口序号)
        jsonStr = HD通用_获取最近返回Json(g_全局窗口序号)
        print(f"切换前 HD识字_获取当前字库:{ret},json:{jsonStr}")

        ret = HD识字_切换字库序号(g_全局窗口序号,3)
        print(f"HD识字_切换字库序号:{ret}")
        ret = HD识字_获取当前字库序号(g_全局窗口序号)#看一看默认的序号？
        print(f"切换后 HD识字_获取当前字库序号:{ret}")

        ret = HD识字_获取当前字库(g_全局窗口序号)
        jsonStr = HD通用_获取最近返回Json(g_全局窗口序号)
        print(f"切换后 HD识字_获取当前字库:{ret},json:{jsonStr}")
        #
        ret = HD识字_自动识字Ex(g_全局窗口序号,759,522,324,173,"少".encode("gbk"),"00FFFF-202020",0.9,1,0,0,11,11,0.1,1)
        jsonStr = HD通用_获取最近返回Json(g_全局窗口序号)
        print(f"json:{jsonStr}")
        print(f"HD识字_自动识字Ex:{ret}")  # 大于0 成功 小于等于0失败