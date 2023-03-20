# 用处
1. 通过依次访问的方式，下载一门课的大部分文件，包括 PDF 和 PPT 等
2. 抓取课程目录下的所有纯文本信息

# 缺陷
1. 文件存放目录不能按照抓取内容结构嵌套，只能放在同一文件夹，与浏览器对文件系统的权限有关（系统为了安全）
2. 脚本开始运行后，需要手动进入对应课程目录，才能开始抓取（content），不过并不算麻烦 
3. 脚本抓取页面文本时，只能获取纯文本信息，因此超链接会丢失 [待解决]
4. 不能下载图片文件 [待解决]
5. 如果程序异常终止，再次运行会重新下载所有文件 [待解决]

# 原理
1. 脚本控制浏览器从主文件目录开始，向下级寻找文件和文件夹链接，将所有文件链接收集起来。
2. 脚本初始化了一个浏览器，拥有在`指定目录`存放下载的属性
3. 脚本通过 get 指令依次访问收集的文件链接，即进行下载

# 使用步骤
1. [Optional] 添加 [info.py](./info.py) 的信息，填入学号和密码
2.0 安装 Anaconda 方便配置 Python 环境 (Python3, 以及包括 Selenium 的库)。[linux参考文章](https://learnubuntu.com/install-conda/), [windows参考文章](https://docs.conda.io/en/latest/miniconda.html?ref=learn-ubuntu#windows-installers)  
2.1 在有 Anaconda 的环境下，你可以使用 `conda env create -f environment.yml` 来生成坏境
3. 脚本实际是控制 Chrome 浏览器，因此需要下载相应版本的 Chromedriver.exe， 可以点[这里下载chrome driver](https://chromedriver.chromium.org/downloads)。下载后解压拿到对应的 exe 文件需要添加到 PATH / 路径，或者放到脚本运行目录。如果想使用 Edge 或者 Firefox 浏览器，需要修改代码，但是原理都是相通的。
4. 运行 [download_content.ipynb](./download_content.ipynb) 的第一块代码，根据提示输入信息，脚本会根据提供的课程名在本地创建一个文件夹存放下载的文件，如果文件名有问题，脚本会再次询问课程名称，知道创建成功
5. 脚本打开bb后，会进行登录，接着需要手动操作控制浏览器进入课程的含内容的目录（不是主页 homepage）
6. 运行脚本的第二块block，这里脚本会从当前页面中获得所有可下载文件的链接，以及下级文件夹的入口，并对深层的目录重复上面的行为。待所有目录都访问完毕后，浏览器会依次访问文件url，因为对被控浏览器的Option属性特殊，浏览器会直接下载文件到本地目录而并不打开对应页面。
7. 等待两三分钟，程序结束

# 测试结果
在windows笔记本上，对 CSC3100 和 EIE3280 的 content 主页使用没问题，可以下载所有pdf和PPT文件
不能下载 PNG 图片，不能下载视频


# 其他
1. Selenium基础教程可以参考[这篇博客](https://cuiqingcai.com/2599.html)
2. Chrome dirver 的[下载链接](https://chromedriver.chromium.org/downloads)
