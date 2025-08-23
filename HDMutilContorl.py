from HD import *
import datetime
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from HDMutilContolUiFun import *
from HDMutilControlInfo import *
from HDMutilControlCallBack import *
# 使用示例
#force_kill_process(1234)  # 替换为目标进程的 PID

#测试账号:heart
#测试密码:111
#仅用于调试使用,发布版本需要正式账号
#开通正式账号找群主充值获取
#HD官网:www.hdgdk.com
#HD官方群:882724064
#PY模块最新版本:25-02-14-01

#设置DLL路径
#=========================================DLL模块引入>>>>>>>>>>>>自行根据版本选择==
#调试版本X86
HD_Path("./lib/HDDebug.dll")
HD环境_调试模式(True)
#=========================================
#发布版本X86
#HD_Path("./lib/hd.dll")
#HD环境_调试模式(False)
#=========================================
#调试版本X64
#HD_Path("./lib/HDDebugx64.dll")
#HD环境_调试模式(True)
#=========================================
#发布版本X64
#HD_Path("./lib/hd64.dll")
#HD环境_调试模式(False)
#=================================================================================
#32 A W 调试(HD调试版本.dll + vm.dll + EXE) 发布(HD发布版本DLL + EXE)
#64 A W 调试(HD调试版本.dll + vm.dll + EXE) 发布(HD发布版本DLL + EXE)
#

# 多线程框架
# 使用HD自带多线程模块
#登录初始化3个步骤必须执行
print("===================================")
print("如果登录崩溃！！！")
print("说明测试账号当前阶段不可用了")
print("请使用自己的正式账号,找群主充值并注册")
print("===================================")
print("===================================")
ret = HD登录_登录("请填写自己的账号！", "请填写自己的密码！","","",False,False)#成功返回一个当前服务器的HD插件版本
print(ret)
ret = HD登录_获取版本号()
print(ret)
ret = HD登录_获取点数()
print(ret)
ret = HD环境_初始化()#成功返回一个0 窗口序号 中控的窗口的序号
print(ret)
ret = HD驱动_安装()#成功 大于等于0 成功 或者 -1068 已经安装  全局
print(ret)
#后面就可以正常调用HD接口了
HD资源_设置路径A("C:\\hd\\test")


# 创建窗口
if __name__ == '__main__':
    # 启动窗口
    g_window.setupUi(g_mainWindow)#窗口设置
    g_mainWindow.show()#窗口显示
    InitHDWindowsInfo()#对象数组初始化
    g_window.InitList()#初始化列表
    InitHDMutilThread(g_mainWindow.winId())#初始化HD多线程环境
    sys.exit(g_app.exec_())#进入循环



