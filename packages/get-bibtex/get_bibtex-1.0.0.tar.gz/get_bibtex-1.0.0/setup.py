from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    my_long_description = f.read()


setup(
    # 关于classifiers的描述详见如下
    # https://pypi.org/search/?q=&o=&c=Topic+%3A%3A+Software+Development+%3A%3A+Build+Tools
    classifiers=[
        # 属于什么类型
        "Topic :: Software Development :: Libraries :: Python Modules",

        # 发展时期,常见的如下
        # Development Status:: 1 - Planning
        # Development Status:: 2 - Pre - Alpha
        # Development Status:: 3 - Alpha
        # Development Status:: 4 - Beta
        # Development Status:: 5 - Production / Stable
        # Development Status:: 6 - Mature
        # Development Status:: 7 - Inactive
        "Development Status :: 4 - Beta",

        # 许可证信息
        # "License :: OSI Approved :: MIT License",

        # 目标编程语言
        # Programming Language :: C
        # Programming Language :: C++
        # Programming Language :: Python :: 3.4
        # Programming Language :: Python :: 3.5
        # Programming Language :: Python :: 3.6
        # Programming Language :: Python :: 3.7
        # Programming Language :: Python :: 3.8
        # Programming Language :: Python :: 3.9
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

        # 运行的操作系统
        # "Operating System :: POSIX :: Linux",
        # "Operating System :: Microsoft :: Windows",

        # 运行的环境
        # "Environment :: GPU :: NVIDIA CUDA :: 12",

        # 开发的目标用户
        # Intended Audience :: Customer Service
        # Intended Audience :: Developers
        # Intended Audience :: Education
        # ...
        # Intended Audience :: End Users/Desktop
        # Intended Audience :: Financial and Insurance Industry
        # Intended Audience :: Healthcare Industry
        "Intended Audience :: Education",

        # 自然语言
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",

    ],

    # 如果上传时出现ERROR：The user '' isn't allowed to upload to project ''，换个名字，长一点无所谓，不能跟别人重复
    name="get_bibtex",
    version="1.0.0",
    author="Yaowen Liu",
    author_email="153672925@qq.com",
    description="This is a project to get bibtex from CrossRef and Google Scholar",
    long_description=my_long_description,

    # 存放源码的地址，填入gitee的源码网址即可
    # url="https://gitee.com/UnderTurrets/",

    packages=find_packages(),

    # README.md文本的格式，如果希望使用markdown语言就需要下面这句话
    long_description_content_type="text/markdown",
)