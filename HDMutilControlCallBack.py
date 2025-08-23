from HDMutilContolUiFun import *
from HDMutilControlInfo import *
# HD多线程模块相关回调函数
# 模板--------------
# HD多线程_初始化流程回调
# 生成一个全局唯一窗口实例 供给创建主窗口
g_app = QApplication(sys.argv)
g_mainWindow = QMainWindow()
g_window = HDMTUi_MainWindow()
# UI回调
@ HD_UiFunType_stdcall
def UICallBack(windows_index, step_text, end1, pause1, thread_state1, end2, pause2, thread_state2):# windows_index 只包含 主(1-61) 序号
    print(f"UI回调: {windows_index}")
    # 更新UI list
    # g_window.startBtn.setText(str(GLOBAL_CLASS_ARRAY[0].id))
    # g_window.accountTableWidget.setItem(windows_index - 1, 4, QTableWidgetItem(step_text.decode('gbk')))
    index = windows_index - 1
    if index < 0:
        return 0
    # 触发UI回调更新UI(主线程)
    global  g_hHDWindowsInfoArray
    info = g_hHDWindowsInfoArray[index]
    # 使用列表管理列创建逻辑
    columns = [
        (0, str(info.windIndex)),
        (1, info.account),
        (2, info.password),
        (3, f"{info.等级}|{info.金币}|{info.钻石}|({info.x},{info.y},{info.z})"),
        (4, step_text.decode('gbk')),  # 操作列
        (5, f"[主] P:{pause1} E:{end1} S:{HD多线程_获取线程状态说明(thread_state1)} | [次] P:{pause2} E:{end2} S:{HD多线程_获取线程状态说明(thread_state2)}"),
        (6, info.IP),
        (7, info.备注)
    ]

    for col_idx, value in columns:
        item = g_window.accountTableWidget.item(index, col_idx)
        item.setText(value)
        g_window.accountTableWidget.setItem(index, col_idx, item)
    return 0

@ HD_ProcessFunType_stdcall
def LoginCallBack(windows_index):# windows_index 只包含 主(1-61) 序号
    print(f"登录回调: {windows_index}")
    #执行登录逻辑
    return 0


@ HD_ProcessFunType_stdcall
def FirstCallBack(windows_index):# windows_index 只包含 主(1-61) 序号
    print(f"执行回调: {windows_index}")
    index = 0
    while HD多线程_是否运行中():
        print(f"执行回调执行中: {index}")
        index = index+1
        HD多线程_延迟(1000)
        HD多线程_发送文本(windows_index, f"执行回调执行中: {index}", False)
        #执行一些自己业务逻辑

    return 0


@ HD_ProcessFunType_stdcall
def SecondCallBack(windows_index):# windows_index 只包含 主(1-61) 序号
    print(f"检查回调: {windows_index}")
    index = 0
    while HD多线程_是否运行中():
        print(f"检查回调执行中: {index}")
        index = index + 1
        HD多线程_延迟(1000)
        # 执行一些自己检查逻辑
    return 0


@ HD_ProcessFunType_stdcall
def StopCallBack(windows_index):# windows_index 只包含 主(1-61) 序号
    print(f"停止回调: {windows_index}")
    # 停止会触发
    return 0


@ HD_ProcessFunType_stdcall
def RestartCallBack(windows_index):# windows_index 只包含 主(1-61) 序号
    print(f"重启回调: {windows_index}")
    # 重启前会触发
    return 0


# HD多线程_初始化操作回调
@ HD_OperationFunType_stdcall
def EndCallBack(index):# index 包含 主(1-61) 副(63-123) 序号
    print(f"结束回调: {index}")
    HD多线程_发送文本(index, f"结束回调: {index}", False)
    # 结束执行会触发
    return 0


@ HD_OperationFunType_stdcall
def PauseCallBack(index):# index 包含 主(1-61) 副(63-123) 序号
    print(f"暂停回调: {index}")
    HD多线程_发送文本(index, f"暂停回调: {index}", False)
    # 暂停执行会触发
    return 0


@ HD_OperationFunType_stdcall
def RecoverCallBack(index):# index 包含 主(1-61) 副(63-123) 序号
    print(f"恢复回调: {index}")
    HD多线程_发送文本(index, f"恢复回调: {index}", False)
    # 恢复执行会触发
    return 0



def InitHDMutilThread(hwnd):
    # 初始化多线程模块 设置各种回调接口
    ret = HD多线程_初始化流程回调(int(hwnd), UICallBack, LoginCallBack, FirstCallBack, SecondCallBack, StopCallBack, RestartCallBack)
    print(f"HD多线程_初始化流程回调:{ret} hwnd:{int(hwnd)}")
    ret = HD多线程_初始化操作回调(EndCallBack, PauseCallBack, RecoverCallBack)
    print(f"HD多线程_初始化操作回调:{ret}")
