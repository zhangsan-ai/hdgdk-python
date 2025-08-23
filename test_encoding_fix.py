#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试编码修复的脚本
"""

import sys
import os

# 添加HD模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from HD.config import auto_encode

def test_auto_encode():
    """测试auto_encode函数"""
    print("=== 测试 auto_encode 函数 ===")
    
    # 测试用例
    test_cases = [
        "Hello World",  # 英文
        "执行回调执行中: 1",  # 中文
        "Test 测试",  # 中英混合
        "123456",  # 数字
        "Special!@#$%^&*()",  # 特殊字符
        "",  # 空字符串
    ]
    
    for i, text in enumerate(test_cases, 1):
        try:
            result = auto_encode(text)
            print(f"测试 {i}: '{text}' -> {result} (长度: {len(result)})")
        except Exception as e:
            print(f"测试 {i}: '{text}' -> 错误: {e}")
    
    # 测试错误类型
    print("\n=== 测试错误处理 ===")
    try:
        auto_encode(123)  # 应该抛出TypeError
    except TypeError as e:
        print(f"类型错误测试通过: {e}")
    except Exception as e:
        print(f"意外错误: {e}")

def test_hd_function_signature():
    """测试HD多线程_发送文本函数签名"""
    print("\n=== 测试函数签名 ===")
    try:
        # 只是导入和检查函数签名，不实际调用
        from HD.HD多线程 import HD多线程_发送文本
        print("HD多线程_发送文本 函数导入成功")
        print(f"函数签名: {HD多线程_发送文本.__annotations__}")
        
        # 模拟调用参数验证（不实际调用HD.dll）
        window_index = 1
        text = "测试文本"
        async_send = False
        
        # 验证参数类型
        if isinstance(window_index, int) and isinstance(text, str) and isinstance(async_send, bool):
            print("参数类型验证通过")
        else:
            print("参数类型验证失败")
            
    except ImportError as e:
        print(f"导入失败: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

if __name__ == "__main__":
    print("开始测试编码修复...")
    test_auto_encode()
    test_hd_function_signature()
    print("\n测试完成！") 