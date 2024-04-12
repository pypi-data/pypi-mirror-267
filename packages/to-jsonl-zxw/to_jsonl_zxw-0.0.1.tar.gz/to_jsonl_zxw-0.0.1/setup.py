"""
# File       : setup.py.py
# Time       ：2024/4/12 上午8:51
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.10
# Description：
"""
from setuptools import setup, find_packages

setup(
    name="to_jsonl_zxw",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        # 依赖的其他包，例如：'requests>=2.0.0'
    ],
    author="XueWei Zhang",
    author_email="tonson_predict@qq.com",
    description="jsonl转换工具",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
