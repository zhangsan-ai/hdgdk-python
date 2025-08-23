from HD import *
import sys

# 结构体数组信息
# 定义结构体（显式指定4字节对齐）
#全局 对象数组 保存各种信息

class HDWindowsInfo:
    def __init__(self, index):
        self.windIndex = index
        self.account = ""
        self.password = ""
        self.等级 = 0
        self.金币 = 0
        self.钻石 = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.IP = ""
        self.备注 = ""


g_hHDWindowsInfoArray = [HDWindowsInfo(i+1) for i in range(HD配置.HD多开数量.value)]


def InitHDWindowsInfo():
    #初始化对象数组
    for index in range(HD配置.HD多开数量.value):
         g_hHDWindowsInfoArray[index].windIndex = index+1
         g_hHDWindowsInfoArray[index].account = "382856600"
         g_hHDWindowsInfoArray[index].password = "1809096"
         g_hHDWindowsInfoArray[index].等级 = index+1
         g_hHDWindowsInfoArray[index].金币 = index+2
         g_hHDWindowsInfoArray[index].钻石 = index+3
         g_hHDWindowsInfoArray[index].x = index+4
         g_hHDWindowsInfoArray[index].y = index+5
         g_hHDWindowsInfoArray[index].z = index+6
         g_hHDWindowsInfoArray[index].IP = "0.0.0.0:123"
         g_hHDWindowsInfoArray[index].备注 = "测试"
