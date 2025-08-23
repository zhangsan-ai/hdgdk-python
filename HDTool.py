# ============================================系统命令强制结束进程
import os
os.system(f"taskkill /PID {pid} /F")


# ============================================模块强制结束进程
import psutil

def force_kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.kill()  # 强制终止
        print(f"进程 {pid} 已终止")
    except psutil.NoSuchProcess:
        print(f"进程 {pid} 不存在")
    except psutil.AccessDenied:
        print(f"权限不足，无法终止进程 {pid}")



# ============================================打印时间 超时检查
import datetime
import time

timeout = datetime.timedelta(seconds=30)  # 设置超时为30秒
start_time = datetime.datetime.now()

while True:
    # 执行其他操作（如检查文件、API响应等）
    current_time = datetime.datetime.now()
    if current_time - start_time > timeout:
        print("操作超时！")
        break
    time.sleep(1)  # 避免CPU满载

