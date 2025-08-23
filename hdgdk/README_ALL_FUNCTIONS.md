# HD GDK 全函数导入功能说明

本文件详细介绍 HD GDK 的全函数导入功能，帮助用户实现无需任何前缀的DLL函数调用方式。

## 功能概述

HD GDK 的全函数导入功能允许用户通过一条导入语句获取所有 HD GDK DLL函数，然后直接调用这些DLL函数，无需任何模块前缀。这种方式特别适合那些希望快速使用 HD GDK 功能的用户。

## 使用方法

### 一次性导入所有DLL函数

最直接的使用方式是通过 `from hdgdk.all_functions import *` 导入所有DLL函数：

```python
# 一次性导入所有 HD GDK DLL函数
from hdgdk.all_functions import *

# 初始化 DLL（实际使用时需要提供正确的 DLL 路径）
init_hdgdk(dll_path="path/to/hdgdk.dll")

# 直接调用DLL函数，无需任何前缀
result = HCHD_Login(b"account", b"password", b"app_name", b"app_lparam", False, False)
expired_time = HCHD_GetExpiredTimeStamp()
```

## 支持的DLL函数列表

通过全函数导入功能，你可以直接使用以下类型的DLL函数：

- 初始化函数：`init_hdgdk`
- Login模块DLL函数：`HCHD_Login`, `HCHD_GetLastLoginFYI`, `HCHD_GetExpiredTimeStamp`, `HCHD_GetFYI`, `HCHD_GetOpenMaxNum`
- IP模块DLL函数：`HCIP_YMSetRootPath`, `HCIP_YMAddIP`, `HCIP_YMAddProcess`, `HCIP_YMOpen`, `HCIP_YMIsOpen`, `HCIP_YMClose`
- Basic模块DLL函数：`HD_Basic_GetVersion`, `HD_Basic_GetBuildDate`, `HD_Basic_GetPlatformInfo`
- Inject模块DLL函数：`HD_Inject_DLL`, `HD_Inject_EjectDLL`
- Env模块DLL函数：`HD_Env_GetVar`, `HD_Env_SetVar`
- MT模块DLL函数：`HD_MT_CreateThread`, `HD_MT_TerminateThread`
- HK模块DLL函数：`HD_HK_Function`, `HD_HK_UnhookFunction`
- Common模块DLL函数：`HD_Common_StringToWString`, `HD_Common_WStringToString`
- ShellCode模块DLL函数：`HD_SH_ExecuteShellCode`
- Yolo模块DLL函数：`HD_YOLO_DetectObjects`
- VNC模块DLL函数：`HD_VNC_CreateSession`, `HD_VNC_CloseSession`
- Win模块DLL函数：`HD_WIN_GetWindowInfo`, `HD_WIN_SendMessage`
- VT模块DLL函数：`HD_VT_Query`, `HD_VT_Protect`
- Lua模块DLL函数：`HD_LUA_ExecuteScript`, `HD_LUA_CallFunction`
- 其他模块DLL函数：`HD_Normal_Operation`, `HD_PP_ProcessProtection`, `HD_TARGET_GetInfo`, `HD_TARGET_Set`, `HD_NT_APICall`, `HD_Core_Operation`, `HD_Memory_Operation`, `HD_File_Operation`, `HD_FS_Operation`, `HD_COM_Operation`, `HD_CS_Operation`, `HD_FI_FileInfo`, `HD_SC_SystemCall`等

## 注意事项

1. **初始化要求**：在调用任何函数之前，必须先使用 `init_hdgdk()` 初始化 DLL

2. **函数名冲突**：由于所有函数都被导入到全局命名空间，请注意可能的函数名冲突问题

3. **代码可读性**：虽然这种方式使用起来很方便，但可能会降低代码的可读性。对于复杂的项目，建议使用模块级调用或直接函数导入

4. **DLL路径**：`init_hdgdk()` 函数需要提供正确的 DLL 路径才能正常工作

5. **函数可用性**：实际可用的函数取决于 HD GDK 的版本和配置

## 与其他调用方式的比较

| 调用方式 | 优点 | 缺点 |
|---------|------|------|
| **全函数导入** | 使用最便捷，无需任何前缀 | 可能导致命名空间污染，降低代码可读性 |
| **直接函数导入** | 明确指定使用哪些函数，避免命名冲突 | 需要列出所有需要使用的函数 |
| **模块级调用** | 代码结构清晰，避免命名冲突 | 需要使用模块名作为前缀 |
| **类实例调用** | 最灵活，支持面向对象编程 | 语法较复杂，需要先创建实例 |

## 示例代码

以下是使用全函数导入功能的完整示例：

```python
# 导入所有HD GDK函数
from hdgdk.all_functions import *

# 初始化HD GDK DLL
try:
    # 提供正确的DLL路径
    dll_path = "path/to/hdgdk.dll"
    init_hdgdk(dll_path=dll_path)
    print("HD GDK 初始化成功！")

except Exception as e:
    print(f"HD GDK 初始化失败: {e}")
    exit(1)

# 使用Login模块函数
try:
    # 调用登录函数，无需前缀
    result = HCHD_Login(b"username", b"password", b"MyApp", b"", False, False)
    if result:
        print("登录成功！")
        # 调用获取登录信息的函数
        login_info = HCHD_GetLastLoginFYI()
        print(f"登录信息: {login_info}")
    else:
        print("登录失败！")

except Exception as e:
    print(f"登录过程中发生错误: {e}")

# 使用IP模块函数
try:
    # 初始化IP模块
    HCIP_YMSetRootPath(b"path/to/ip_data")
    HCIP_YMOpen()
    print("IP模块初始化成功！")
    
    # 添加IP和进程
    HCIP_YMAddIP(b"192.168.1.1")
    HCIP_YMAddProcess(1234) # 进程ID
    
    # 使用完毕后关闭IP模块
    HCIP_YMClose()
    

except Exception as e:
    print(f"IP模块操作过程中发生错误: {e}")

# 使用Basic模块函数
try:
    # 获取版本信息
    version = HD_Basic_GetVersion()
    build_date = HD_Basic_GetBuildDate()
    platform_info = HD_Basic_GetPlatformInfo()
    
    print(f"HD GDK 版本: {version}")
    print(f"构建日期: {build_date}")
    print(f"平台信息: {platform_info}")

except Exception as e:
    print(f"获取Basic信息过程中发生错误: {e}")
```

## 常见问题解答

**Q: 为什么我导入后无法调用某些函数？**
**A:** 可能的原因包括：
- DLL 未正确初始化
- 该函数在当前版本的 HD GDK 中不可用
- 函数名拼写错误

**Q: 这种导入方式会影响性能吗？**
**A:** 不会直接影响性能，但会增加命名空间的大小。如果项目中使用了大量不同来源的函数，可能会导致命名冲突。

**Q: 我可以同时使用全函数导入和其他导入方式吗？**
**A:** 是的，你可以根据需要混合使用不同的导入方式。但请注意避免命名冲突。