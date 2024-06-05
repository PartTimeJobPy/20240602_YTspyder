### 创建python虚拟环境

安装python3.10

访问https://www.python.org/downloads/macos/

选择与系统匹配的python310文件 如：[macOS 64-bit universal2 installer](https://www.python.org/ftp/python/3.10.5/python-3.10.5-macos11.pkg)



安装并打开终端



终端命令：



1. cd ~
2. pip3 config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple
3. pip install virtualenv
4. virtualenv spyder
5. source ~/.env/spyder/bin/activate
6. cd 202400602_YTspyder
7. pip install -r reqestments.txt



### 下载谷歌浏览器驱动

查看Google浏览器的版本信息，然后访问网站下指定版本驱动，如124.0.xxxx, 

[网站]: https://getwebdriver.com/chromedriver

解压文件后，把chromedriver.exe文件放到202400602_YTspyder文件中。



查看源代码，推荐使用pycharm 或vscode, 主代码是main.py文件



