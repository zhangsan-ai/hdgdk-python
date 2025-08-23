#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HD-Python模块DLL加载使用示例
演示如何正确设置调试模式和使用HD环境_调试模式函数
"""

from HD import *
HD_Path("./lib",True) #设置路径和调试模式
HD环境_调试模式() #无需传参通过HD_Path获取
ret = HD登录_登录("","","","")
print(ret)