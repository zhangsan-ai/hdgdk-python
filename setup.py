from setuptools import setup, find_packages
import os

# 获取当前目录
here = os.path.abspath(os.path.dirname(__file__))

# 读取README文件内容作为long_description
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

def get_version():
    """从版本文件或直接返回默认版本"""
    # 这里可以从版本文件中读取，或者直接返回默认版本
    return '1.0.0'

setup(
    name='HD-Python',  # PyPI上的包名
    version=get_version(),  # 版本号
    description='HD引擎Python调用模块',  # 简短描述
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/YOUR_USERNAME/HD-Python',  # 项目URL
    author='开发者名称',
    author_email='your.email@example.com',
    license='MIT',  # 许可证
    packages=find_packages(),  # 自动发现所有包
    include_package_data=True,
    install_requires=[
        # 列出项目依赖
        # 这个项目主要依赖标准库，但可能需要以下依赖
        # 'numpy>=1.19.5',  # 如果项目使用了numpy
    ],
    data_files=[
        ('lib', ['lib/hd.dll', 'lib/HDDebug.dll', 'lib/VMProtectSDK32.dll'])
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',  # 最低Python版本要求
    keywords='hd, automation, windows, api',
    project_urls={
        'Bug Reports': 'https://github.com/YOUR_USERNAME/HD-Python/issues',
        'Source': 'https://github.com/YOUR_USERNAME/HD-Python',
    },
)