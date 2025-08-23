from HD import *
import datetime
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from hduifun import HDUi_MainWindow


# 使用示例
#force_kill_process(1234)  # 替换为目标进程的 PID

#测试账号:heart
#测试密码:111
#仅用于调试使用,发布版本需要正式账号
#开通正式账号找群主充值获取
#HD官网:www.hdgdk.com
#HD官方群3:882724064
#HD官方群5:1030698387
#PY模块最新版本:25-08-10-01

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

#第一节  放在窗口创建完成后的流程中
#登录初始化3个步骤必须执行
print("如果登录崩溃！！！")
print("说明测试账号当前阶段不可用了")
print("请使用自己的正式账号,找群主充值并注册")
ret = HD登录_登录("请填写自己的账号！", "请填写自己的密码！","","",False,False)#成功返回一个当前服务器的HD插件版本
print(ret)
ret = HD登录_获取点数()
print(ret)
ret = HD环境_初始化()#成功返回一个0 窗口序号 中控的窗口的序号
print(ret)
ret = HD驱动_安装()#成功 大于等于0 成功 或者 -1068 已经安装  全局
print(ret)
#后面就可以正常调用HD接口了
HD资源_设置路径A("C:\\hd\\test")

#创建窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    window = HDUi_MainWindow()
    window.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())



