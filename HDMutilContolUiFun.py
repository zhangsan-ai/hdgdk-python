from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QMainWindow,QAbstractItemView,QCheckBox,QTabBar
from hdqtcontrolui import *
from HDMutilControlInfo import *
from PyQt5.QtCore import Qt  # 关键导入
from HD import *
import datetime
import time
import sys


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





class HDMTUi_MainWindow(Ui_MainWindow):

    # 静态变量 操作计数
    s_indexOpration = 1

    # 初始化list
    def InitList(self):
        global  g_hHDWindowsInfoArray
        valid_count = min(HD配置.HD多开数量.value, len(g_hHDWindowsInfoArray))
        for index in range(valid_count):
            info = g_hHDWindowsInfoArray[index]
            self.accountTableWidget.insertRow(index)
            # 使用列表管理列创建逻辑
            columns = [
                (0, str(info.windIndex)),
                (1, info.account),
                (2, info.password),
                (3, f"{info.等级}|{info.金币}|{info.钻石}|({info.x},{info.y},{info.z})"),
                (4, ""),  # 操作列
                (5, "[主] P:0 E:0 S:未启动 | [次] P:0 E:0 S:未启动"),
                (6, info.IP),
                (7, info.备注)
            ]
            print(f"{index}")
            for col_idx, value in columns:
                #创建新的列
                item = QTableWidgetItem(value)
                #第一列 加上复选框
                if col_idx == 0:
                    item.setCheckState(False)
                self.accountTableWidget.setItem(index, col_idx, item)


    # 窗口配置
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)#调用父类的setupUi
        #在这下面可以 设置一些回调函数 信号槽
        self.startBtn.clicked.connect(self.StartFun)
        self.stopBTn.clicked.connect(self.StopFun)
        self.pauseBtn.clicked.connect(self.PauseFun)
        self.recoverBtn.clicked.connect(self.RecoverFun)
        self.allStartBtn.clicked.connect(self.AllStartFun)
        self.allStopBtn.clicked.connect(self.AllStopFun)
        self.allPauseBtn.clicked.connect(self.AllPauseFun)
        self.allRecoverBtn.clicked.connect(self.AllRecoverFun)
        self.restartBtn.clicked.connect(self.RestartFun)
        # 配置list
        # 初始化list
        #序号 账号 密码 角色信息 操作信息 状态信息 IP 备注
        self.accountTableWidget.setColumnCount(8)
        self.accountTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.accountTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 隐藏垂直表头（行号列）
        self.accountTableWidget.verticalHeader().setVisible(False)
        # 可选样式美化
        self.accountTableWidget.setStyleSheet("""
               QTableWidget {
                   font-size: 12px;
                   gridline-color: #E0E0E0;
               }
               QTableWidget::item:selected {
                   background-color: #E1F5FE;
                   color: black;
               }
           """)
        # 2. 设置列头文本
        column_headers = ["序号", "账号", "密码", "角色信息", "操作信息", "状态信息", "IP", "备注"]
        self.accountTableWidget.setHorizontalHeaderLabels(column_headers)
        # 3. 可拖动
        self.accountTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # 4. 调整列宽
        self.accountTableWidget.setColumnWidth(0, 50)
        self.accountTableWidget.setColumnWidth(1, 80)
        self.accountTableWidget.setColumnWidth(2, 80)
        self.accountTableWidget.setColumnWidth(3, 220)
        self.accountTableWidget.setColumnWidth(4, 320)
        self.accountTableWidget.setColumnWidth(5, 350)
        self.accountTableWidget.setColumnWidth(6, 100)
        self.accountTableWidget.setColumnWidth(7, 100)


    # 日志添加接口
    def Append_log(self,text):
        self.logEdit.insertPlainText(text)
        self.logEdit.verticalScrollBar().setValue(
            self.logEdit.verticalScrollBar().maximum()
        )

    # 单个开启
    def StartFun(self):
        #HD多线程_开启窗口(1)
        #HD多线程_发送文本(1,"测试".encode(),False)
        selected_items = self.accountTableWidget.selectedItems()
        index = selected_items[0].row() if selected_items else -1
        if (index != -1):
            HD多线程_开启窗口(g_hHDWindowsInfoArray[index].windIndex)
            self.Append_log(f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_开启窗口:" + str(g_hHDWindowsInfoArray[index].windIndex) + "\n")
        else:
            self.Append_log(f"{HDMTUi_MainWindow.s_indexOpration}请选择需要登录的窗口序号:\n")

        #累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1

        # 单个开启接口

    # 单个停止
    def StopFun(self):
        selected_items = self.accountTableWidget.selectedItems()
        index = selected_items[0].row() if selected_items else -1
        if (index != -1):
            HD多线程_停止窗口(g_hHDWindowsInfoArray[index].windIndex)
            self.Append_log(
                f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_停止窗口:" + str(g_hHDWindowsInfoArray[index].windIndex) + "\n")
        else:
            self.Append_log(f"{HDMTUi_MainWindow.s_indexOpration}请选择需要登录的窗口序号:\n")

        # 累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1

    # 单个暂停
    def PauseFun(self):
        selected_items = self.accountTableWidget.selectedItems()
        index = selected_items[0].row() if selected_items else -1
        if (index != -1):
            HD多线程_暂停窗口(g_hHDWindowsInfoArray[index].windIndex)
            self.Append_log(
                f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_暂停窗口:" + str(g_hHDWindowsInfoArray[index].windIndex) + "\n")
        else:
            self.Append_log(f"{HDMTUi_MainWindow.s_indexOpration}请选择需要登录的窗口序号:\n")

        # 累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1

    # 单个恢复
    def RecoverFun(self):
        selected_items = self.accountTableWidget.selectedItems()
        index = selected_items[0].row() if selected_items else -1
        if (index != -1):
            HD多线程_恢复窗口(g_hHDWindowsInfoArray[index].windIndex)
            self.Append_log(
                f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_恢复窗口:" + str(g_hHDWindowsInfoArray[index].windIndex) + "\n")
        else:
            self.Append_log(f"{HDMTUi_MainWindow.s_indexOpration}请选择需要登录的窗口序号:\n")

        # 累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1

    # 单个重启
    def RestartFun(self):
        selected_items = self.accountTableWidget.selectedItems()
        index = selected_items[0].row() if selected_items else -1
        if (index != -1):
            HD多线程_重启窗口MsgEx(g_hHDWindowsInfoArray[index].windIndex,True)
            self.Append_log(
                f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_重启窗口MsgEx:" + str(g_hHDWindowsInfoArray[index].windIndex) + "\n")
        else:
            self.Append_log(f"{HDMTUi_MainWindow.s_indexOpration}请选择需要登录的窗口序号:\n")

        # 累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1

    # 全部开启
    def AllStartFun(self):
        valid_count = min(HD配置.HD多开数量.value, len(g_hHDWindowsInfoArray))
        for index in range(valid_count):
            if self.accountTableWidget.item(index,0).checkState() == Qt.Checked:
                HD多线程_开启窗口(g_hHDWindowsInfoArray[index].windIndex)
                self.Append_log(
                    f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_开启窗口:" + str(
                        g_hHDWindowsInfoArray[index].windIndex) + "\n")

        # 累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1

    # 全部结束
    def AllStopFun(self):
        valid_count = min(HD配置.HD多开数量.value, len(g_hHDWindowsInfoArray))
        for index in range(valid_count):
            if self.accountTableWidget.item(index,0).checkState() == Qt.Checked:
                HD多线程_停止窗口(g_hHDWindowsInfoArray[index].windIndex)
                self.Append_log(
                    f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_停止窗口:" + str(
                        g_hHDWindowsInfoArray[index].windIndex) + "\n")

        # 累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1


    # 全部暂停
    def AllPauseFun(self):
        valid_count = min(HD配置.HD多开数量.value, len(g_hHDWindowsInfoArray))
        for index in range(valid_count):
            if self.accountTableWidget.item(index,0).checkState() == Qt.Checked:
                HD多线程_暂停窗口(g_hHDWindowsInfoArray[index].windIndex)
                self.Append_log(
                    f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_暂停窗口:" + str(
                        g_hHDWindowsInfoArray[index].windIndex) + "\n")

        # 累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1


    # 全部恢复
    def AllRecoverFun(self):
        valid_count = min(HD配置.HD多开数量.value, len(g_hHDWindowsInfoArray))
        for index in range(valid_count):
            if self.accountTableWidget.item(index,0).checkState() == Qt.Checked:
                HD多线程_恢复窗口(g_hHDWindowsInfoArray[index].windIndex)
                self.Append_log(
                    f"{HDMTUi_MainWindow.s_indexOpration}HD多线程_恢复窗口:" + str(
                        g_hHDWindowsInfoArray[index].windIndex) + "\n")

        # 累计操作计数 为了方便日志查看
        HDMTUi_MainWindow.s_indexOpration = HDMTUi_MainWindow.s_indexOpration + 1