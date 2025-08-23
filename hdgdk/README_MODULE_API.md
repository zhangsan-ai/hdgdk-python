# HD GDK 模块级 API 功能说明

本文件详细介绍 HD GDK 的模块级 API 功能，帮助用户更便捷地使用 HD GDK 的各项功能。

## 功能概述

HD GDK 提供了两种主要的 API 调用方式：

1. **直接函数调用**：从 hdgdk 包直接导入并调用单个函数（如 `login`, `get_local_ip` 等）
2. **模块级调用**：一次性导入整个模块，然后调用模块中的函数（如 `login_module.login()`, `ip.get_local_ip()` 等）

本说明主要介绍模块级 API 调用方式。

## 模块级 API 的优势

- **更符合 Python 编程习惯**：使用 `module.function()` 的方式调用函数
- **代码结构更清晰**：按功能模块组织代码，提高可读性和可维护性
- **导入方式更简洁**：一次性导入整个模块，而不是多个独立函数
- **避免函数名冲突**：通过模块名区分同名函数

## 使用方法

### 1. 初始化 HD GDK

在使用任何 HD GDK 功能之前，必须先初始化 DLL：

```python
from hdgdk import init_hdgdk

# 初始化 DLL
# 注意：实际使用时需要提供正确的 DLL 路径
init_hdgdk(dll_path="path/to/hdgdk.dll")
```

### 2. 使用直接导入的模块

目前支持直接导入的主要模块有：

```python
from hdgdk import login_module

# 调用模块中的函数
result = login_module.login(account, password, app_name, app_lparam)
last_fyi = login_module.get_last_login_fyi()
```

### 3. 使用 get_module 函数获取模块

对于大多数模块，建议使用 `get_module()` 函数动态获取：

```python
from hdgdk import get_module

# 获取 IP 模块
ip = get_module('ip')
local_ip = ip.get_local_ip()
public_ip = ip.get_public_ip()

# 获取基础模块
basic = get_module('basic')
version = basic.get_version()

# 获取窗口模块
win = get_module('win')
window_info = win.get_window_info(window_handle)
```

### 4. 支持的模块列表

HD GDK 支持以下主要模块（括号内为模块名称）：

- 登录模块 (login)
- IP 操作模块 (ip)
- 基础功能模块 (basic)
- 注入模块 (inject)
- 环境模块 (env)
- 内存操作模块 (mt)
- 钩子模块 (hk)
- 通用功能模块 (common)
- Shell Code 模块 (shell_code)
- YOLO 模块 (yolo)
- VNC 模块 (vnc)
- Windows 操作模块 (win)
- 虚拟机检测模块 (vt)
- Lua 脚本模块 (lua)
- 常规功能模块 (normal)
- 进程保护模块 (pp)
- 目标管理模块 (target)
- NTAPI 模块 (nt)
- 硬盘操作模块 (hd)
- 模块管理模块 (m)
- 指纹模块 (fp)
- 文件系统模块 (fs)
- COM 模块 (com)
- 反调试模块 (cs)
- 文件操作模块 (fi)
- 系统调用模块 (sc)
- 蓝屏模块 (bs)
- 键盘记录模块 (mkb)
- 注册表模块 (rc)
- 虚拟机模块 (vm)
- VM DMA 模块 (vmdma)
- 游戏保护模块 (gb)
- 驱动服务模块 (ds)
- 资源模块 (res)
- JSON 模块 (json)
- 调试模块 (dw)
- 系统信息模块 (sys)
- 状态模块 (status)

## 注意事项

1. 必须先使用 `init_hdgdk()` 初始化 DLL 后才能调用其他函数
2. 模块名称区分大小写，请使用正确的模块名称
3. 如果获取模块失败，可能是该模块在当前版本的 HD GDK 中不可用
4. 对于 `login` 模块，由于函数名冲突，直接导入时使用 `login_module`
5. 使用 `get_module('login')` 来获取登录模块
6. 实际调用函数时，需要提供正确的参数，具体参数请参考 HD GDK 文档

## 示例代码

```python
from hdgdk import init_hdgdk, login_module, get_module

# 初始化 DLL
init_hdgdk(dll_path="path/to/hdgdk.dll")

# 使用直接导入的 login_module
result = login_module.login("username", "password", "MyApp", 0)
if result:
    print("登录成功!")
    print(f"登录信息: {login_module.get_last_login_fyi()}")

# 使用 get_module 获取其他模块
ip = get_module('ip')
print(f"本地 IP: {ip.get_local_ip()}")
print(f"公网 IP: {ip.get_public_ip()}")

basic = get_module('basic')
print(f"HD GDK 版本: {basic.get_version()}")

win = get_module('win')
# 获取当前窗口信息
current_window_info = win.get_window_info(0)
print(f"当前窗口信息: {current_window_info}")
```

## 常见问题解答

**Q: 为什么我无法获取某个模块？**
**A:** 可能的原因包括：
- 模块名称拼写错误（区分大小写）
- 该模块在当前版本的 HD GDK 中不可用
- DLL 初始化失败或版本不兼容

**Q: 模块级 API 和直接函数调用有什么区别？**
**A:** 两者功能相同，只是调用方式不同。模块级 API 更符合 Python 的编程习惯，组织代码更清晰。

**Q: 我可以混合使用两种 API 调用方式吗？**
**A:** 是的，您可以根据需要混合使用两种调用方式。

**Q: 如果模块中没有某个函数，会发生什么？**
**A:** 尝试访问不存在的函数将会引发 AttributeError 异常。建议在调用前检查函数是否存在。