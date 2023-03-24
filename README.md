# 用处
1. 通过依次访问的方式，下载一门课的大部分文件，包括 PDF 和 PPT 等
2. 抓取课程目录下的所有纯文本信息

# 脚本逻辑
1. 初始一个浏览器，设定在`用户指定目录`存放下载文件的属性
2. 控制浏览器进入 bb 页面后，等待用户点击到对应课程主文件目录，用户在命令行中回车，脚本开始抓取
3. 脚本依次向下级寻找文件和文件夹链接，将所有文件链接收集起来，并去重
3. 脚本通过 get 指令依次访问收集的文件链接，下载也随之开始

# 使用步骤
## 配置个人信息
1. [Optional] 添加 [info.py](./info.py) 的信息，填入学号和密码
## 配置运行环境
2.0 安装 Anaconda 方便配置 Python 环境 (Python3, 以及包括 Selenium 的库)。[linux下安装 Anaconda 参考](https://learnubuntu.com/install-conda/), [windows下安装 Anaconda 参考](https://docs.conda.io/en/latest/miniconda.html?ref=learn-ubuntu#windows-installers)  
2.1 有 Anaconda 后，clone 这个仓库，命令行进入仓库地址后，使用 `conda env create -f environment.yml` 来下载需要环境
3. 因为脚本需要控制 Chrome 浏览器，因此需要 Chrome 浏览器，还要下载与浏览器版本对应的 Chromedriver.exe， 可以在[这里下载chrome driver](https://chromedriver.chromium.org/downloads)。下载后解压拿到对应的 exe 文件放到脚本运行目录，不然需要添加到 PATH / 路径。如果想使用 Edge 或者 Firefox 浏览器，需要修改代码，但是原理都是相通的，改动不会太大，我时间会尝试做兼容的版本。
## 运行脚本 （人工参与）
4. 运行 [main.ipynb](./main.ipynb) 或者 [main.py](./main.py) 的代码，根据提示输入信息，脚本会根据提供的课程名在本地创建一个文件夹存放下载的文件。如果文件名有问题（比如含非法字符），脚本会再次询问课程名称，直到成功创建。
5. 脚本打开bb后，进行登录。登陆完毕，需要你手动控制浏览器进入课程的含主内容目录（不是主页 homepage）。
## 等待脚本运行
6. 继续运行脚本，从当前页面中获得所有可下载文件的链接，以及下级文件夹的入口，并对深层的目录重复上面的行为。待所有目录都访问完毕后，浏览器会依次访问文件url，对应的内容会开始下载。
7. 下载完毕，程序结束

# 测试结果
在windows平台上，对 CSC3100 和 EIE3280 的 content 主页使用没问题，可以下载所有pdf和PPT文件。
在 Chromebook 的虚拟 Linux 机内也能成功运行。

# 缺陷
1. 文件存放目录不能按照抓取内容结构嵌套，只能放在同一文件夹，与浏览器对文件系统的权限有关（系统为了安全）
2. 脚本开始运行后，需要手动进入对应课程目录，才能开始抓取（content），不过并不算麻烦 
3. 脚本抓取页面文本时，只能获取纯文本信息，因此超链接会丢失 [待解决]
4. 不能下载图片文件 [待解决]
5. 如果程序异常终止，再次运行会重新下载所有文件 [待解决]

# 其他
1. Selenium基础教程可以参考[这篇博客](https://cuiqingcai.com/2599.html)
2. Chrome dirver 的[下载链接](https://chromedriver.chromium.org/downloads)
