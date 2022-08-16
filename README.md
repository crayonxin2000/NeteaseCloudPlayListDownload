<center >
<font size="5">【自制脚本】python+IDM批量下载网易云音乐歌单歌曲
</font>
</center>

<br>



<br>

# 声明

> 此脚本仅用作学习交流之用，禁止任何个人及团体利用此脚本进行其他用途。

# 前言
网易云平台的音乐的歌曲需要会员才能下载，而且使用其他工具下载此平台上的音乐大多只能一首一首下载。而我想要的是批量下载整个歌单的音乐。
所以我只做了这个脚本。很便利的下载网易云歌曲。
我已经将脚本文件上传到github仓库中，欢迎交流学习
[python+IDM批量下载网易云音乐歌单歌曲](https://github.com/crayonxin2000/NeteaseCloudPlayListDownload)，这个脚本的详细介绍也可以去仓库里看。


>非常感谢github上的开源api提供的支持，web请求使用的是此api
> [网易云 NodeJS 版 API](https://github.com/Binaryify/NeteaseCloudMusicApi)

# 预览
使用的python工具，运行  `python musics.py`,然后一步步按提示做就可以了

![在这里插入图片描述](https://img-blog.csdnimg.cn/e2f185077fe241ebbdedfe5748a1786c.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NyYXlvbnhpbjIwMDA=,size_16,color_FFFFFF,t_70#pic_center)

下载的歌曲会自己重命名。

![在这里插入图片描述](https://img-blog.csdnimg.cn/c1806f49550f4f8486ccb64b12ec3a96.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NyYXlvbnhpbjIwMDA=,size_16,color_FFFFFF,t_70#pic_center)
# 环境要求

 1. python3
 2. python的一些库：requests；subprocess；tqdm
（没有的使用pip安装，在requirements.txt已列出）
```python
import os
import json
import traceback
import requests
import time
import sys
from subprocess import call
from tqdm import tqdm
import cv2
import base64
import skimage.io
```

 
 4. IDM
（歌单一般包含大量歌曲，使用idm多线程下载较好，而且idm应该电脑必备吧，用的人多。）
# 安装
**方式1：**
 点击下方链接下载.py文件
[python+IDM批量下载网某平台音乐歌单歌曲](https://github.com/crayonxin2000/NeteaseCloudPlayListDownload)
文件放的位置无所谓。
**方式2**

<br>

# 使用方法

## 1、cmd启动脚本
调出cmd，cd切到文件所在目录，并输入python musics.py
如下图

![python musics.py](https://img-blog.csdnimg.cn/625f8ec8ea524525897e3b50b50423d3.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NyYXlvbnhpbjIwMDA=,size_16,color_FFFFFF,t_70#pic_center)
##  2、登录
<font color="#ee0000">**如果你要下载自己创建的歌单，一定要登录!** </font>

如果你下载的是那种公共的歌单（好几万播放量那种），是不用登录也可以下载的。

输入“y”或者"n"

我输入“y”
在第一版中我使用账号密码登录，但是考虑到安全性，我再第二版换成了扫描二维码登录，这样更加方便一些

![在这里插入图片描述](https://img-blog.csdnimg.cn/2d018c2c0c574e9db537aceb4b98162e.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NyYXlvbnhpbjIwMDA=,size_16,color_FFFFFF,t_70#pic_center)



##  3、输入歌单id
输入歌单id，然后按回车键，脚本会收集歌单中所有歌曲的信息
如下图

![在这里插入图片描述](https://img-blog.csdnimg.cn/b9c1c1480bbe40a889a53f0bfd8c8e3b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAQ3JheW9u6ZGr,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
注意：这里的进度条不是下载的进度条，这是分析id得到歌单下所有歌曲信息的进度条。你歌单的音乐越多，这步花费的时间越长。进度完成之后，会提示你是否下载。

补充：如果你不知道歌单的id怎么获取，请在文末“[补充-获取歌单id](#getid)”一节中了解。
##  4、下载
会提示你是否下载
输入“y”
会提示文件保存路径和idm安装路径。
一般这俩不用管，一直回车就行。

![在这里插入图片描述](https://img-blog.csdnimg.cn/e994ab66ab624bbab11c772c365b4d6f.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NyYXlvbnhpbjIwMDA=,size_16,color_FFFFFF,t_70#pic_center)
将下载队列添加到idm中，脚本的使命就完成了。
剩下的活交给idm就行了。
## 5、等待。。。
不一会，idm队列就开始工作了，耐心等待下载就行了

![在这里插入图片描述](https://img-blog.csdnimg.cn/8239fb0035fe440fbad2efd744fa8e1f.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NyYXlvbnhpbjIwMDA=,size_16,color_FFFFFF,t_70#pic_center)
歌曲保存在以歌单名为名的文件夹。

<hr>

# 源码分析
脚本比较简单，就是调用一些api。
以下是比较重要的方法

```python
# 判断密码是否正确
def confirmPassword(name,password,data):
#验证cookie可用性
def confirmCookie(cookies):
# 登录方法
def login():
# 获取歌单详情(包括介绍，名字等等)
def getListDetail(ids,cookie):
# 获取音乐真实下载地址
def getMusicUrl(id,cookie):
# 打包歌单的歌曲下载链接、歌名等，返回的是json数组对象 # 过程时间比较长，需要进度条
def publishDownLoad(ids,cookie) :
# idm下载
def IDMdownload(dl,file):
```
在这里贴一下idm下载的方法：

```python
def IDMdownload(dl,file):# dl参数是列表，每个列表项为字典
    idm_path=input("请输入idm软件存放地点，直接回车将使用默认路径")
    if idm_path=="":
        IDM = 'C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe'
    else:
        IDM=idm_path
    if os.path.exists(IDM):
        print("idm下载中......")
        down_path = file+"\\"+ReplaceName(playlistName).strip()
        # 建立文件夹
        if os.path.exists(down_path):
            pass
        else:
            os.mkdir(down_path)
        for i in dl:
            if i["url"]!=None:
                down_url = i["url"]
                str=i["name"]
                name=ReplaceName(str)
                output_filename=name.strip()+".mp3"
                call([IDM, '/d',down_url, '/p',down_path, '/f', output_filename, '/n', '/a'])
        print("idm正在下载，请打开idm查看下载进度")
    else:
        print("IDM程序不存在，将使用普通下载")
        Comdownload(dl,file)

```
<br/>
<hr/><br/>

# 补充
##  6. <a name='-&nbsp;-&nbsp;如何获取歌单id'></a>  &nbsp; &nbsp;如何获取歌单id 
<div id="getid"></div>

###  6.1. <a name='&nbsp;&nbsp;&nbsp;&nbsp;分享链接'></a>&nbsp;&nbsp;&nbsp;&nbsp;分享链接
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;点击分享，点击“复制链接”

![分享链接](https://img-blog.csdnimg.cn/e681b4bd52ea4183afc63b6ad7a76475.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NyYXlvbnhpbjIwMDA=,size_16,color_FFFFFF,t_70#pic_center)
###  6.2. <a name='&nbsp;&nbsp;&nbsp;&nbsp;提取链接中的id字段'></a>&nbsp;&nbsp;&nbsp;&nbsp;提取链接中的id字段
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;将复制的文本粘贴在一个地方，你会看到链接中有“id=xxxxxx”字样
那个数字就是歌单id
![在这里插入图片描述](https://img-blog.csdnimg.cn/3a953924e86d405b8606c625499470a1.png#pic_center)
# 总结
总体说来这个脚本比较简单，可以下载网某云歌单中的歌曲。但是，网易云无版权的歌曲是下载不了的。
有不明白的地方可以私信或者评论，我都尽可能答复的。

![在这里插入图片描述](https://img-blog.csdnimg.cn/13262acf8b634bd0977282ce2cc5dc6d.jpg#pic_center)
