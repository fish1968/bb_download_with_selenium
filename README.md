# 用处
快速下载 Blackboard 上某一门课的大部分 pdf/ppt 之类的文件

# 缺陷
1. 一次只能在一块目录进行下载
2. 需要手动找到对应课程含内容的目录

# 使用步骤
1. 添加 [info.py](./info.py) 的信息，填入学号和密码
2. 安装 Anaconda 配置好 Python 环境 (Python3, 以及库包括 Selenium)
3. 脚本实际是控制 Chrome 浏览器，因此安装版本匹配的 Chromedriver.exe。如果想使用 Edge 或者 Firefox 浏览器，需要修改代码，但是原理应该都是相通的，改变不会太多。
4. 运行 [download_content.ipynb](./download_content.ipynb) 的第一块代码，根据提示输入信息，脚本根据提供的课程名在本地创建一个文件夹存放下载的文件
5. 脚本打开bb后，会进行登录，接着需要手动操作控制浏览器进入课程的含内容的目录（不是主页 homepage）
6. 运行脚本的第二块block，这里脚本会从当前页面中获得所有可下载文件的链接，以及下级文件夹的入口，并对深层的目录重复上面的行为。待所有目录都访问完毕后，浏览器会依次访问文件url，因为对被控浏览器的Option属性特殊，浏览器会直接下载文件到本地目录而并不打开对应页面。
7. 等待两三分钟，程序结束


# 测试结果
在windows笔记本上，对 CSC3100 和 EIE3280 的 content 主页使用没问题，可以下载所有pdf和PPT文件
但不能下载视频文件

# 其他
1. Selenium基础教程可以参考[这篇博客](https://cuiqingcai.com/2599.html)