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

# from requests.api import get, head
host="https://netease-cloud-music-api-gamma-orpin.vercel.app" # 网易云api地址
header={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"} # 请求头
config_="user.json" # 配置文件

# 判断密码是否正确      #————————已废弃
# def confirmPassword(name,password,data):
#     '''验证账号和密码是否有误
#     以后使用二维码登录，此函数失效
#     '''
#     url=host
#     d={}
#     if "@" in name:
#         url+="/login"
#         d["email"]=name
#     else :
#         url+="/login/cellphone"
#         d["phone"]=name
#     d["password"]=password
#     t=int(time.time())
#     url+="?timestamp="+str(t)
#     response = requests.post(url,data=d,headers=header)
#     json_obj=json.loads(response.text)
#     if json_obj["code"]==502:
#         print("密码错误")
#         inputAgain(data)
#         return False
#     elif json_obj["code"]==200:
#         print("密码正确")
#         data["cookie"]=json_obj["cookie"]
#         return True
#     else:
#         print("登录出错")
#         inputAgain(data)
        
#验证cookie可用性
def confirmCookie(cookies):
    t=int(time.time())
    url=host+"/login/status?timestamp="+str(t)
    response = requests.get(url,headers=header,cookies=cookies)
    json_obj=json.loads(response.text)
    # print(response.text)
    nickname=json_obj["data"]["profile"]["nickname"]
    print(f"欢迎您：{nickname}")
    if json_obj["data"]["account"]==None:
        return False
    else:
        return True

# def inputAgain(data):    #======已废弃=======
#     data["name"]=input("请重新输入您的网易云账号（支持电话，邮箱）")
#     data["password"]=input("请重新输入您的网易云密码")
#     confirmPassword(data["name"],data["password"],data)

def getCookieDict(cook):
    '''将cookie字符串格式化为字典型变量
    '''
    cookies={}#初始化cookies字典变量
    for line in cook.split(';'):   #按照字符：进行划分读取
        #其设置为1就会把字符串拆分成2份
        if line!="":
            # print(line)
            if "=" in line:
                name,value=line.strip().split('=')
                cookies[name]=value  #为字典cookies添加内容
    return cookies

# 登录方法     #========已废弃========
# def login():
#     try:
#         r= open(config_,"r")
#         s=r.read()
#         # print(s)
#         data=json.loads(s)
#         # 判断用户名是否存在
#         if "name" in data:
#             print("当前账户:"+data["name"])
#         else:
#             data["name"]=input("请输入您的网易云账号（支持电话，邮箱）")
#         name=data["name"] 
#         # 判断密码是否存在
#         if "password" in data:
#             print("密码已保存")
#         else:
#             data["password"]=input("请输入您的网易云密码")
#         password=data["password"]
#         # 判断密码是否正确
#         confirmPassword(name, password,data)
#         # 还需要将配置保存
#         w=open(config_,"w")
#         w.write(json.dumps(data))
#         w.close()
#         cookie=""
#         if "cookie" in data:
#             cookie=data["cookie"]
#         return cookie
#     except Exception as ex :
#         print(traceback.format_exc()) 

def loginByQR():
    '''二维码登录
    '''
    cookie_str=""
    # 获取二维码key
    url=host+'/login/qr/key'
    data={"timestamp":time.time()}
    response = requests.post(url,data=data,headers=header)
    re_json=response.json()
    key=re_json["data"].get("unikey") # 获取二维码key
    # 获取二维码图片
    url=host+'/login/qr/create'
    data={"timestamp":time.time(),"key":key,"qrimg":"true"}
    response = requests.post(url,data=data,headers=header)
    re_json=response.json()
    qrimg=re_json["data"]["qrimg"]
    base64_str=qrimg.split(",")[1]
    # 显示二维码图像
    imgdata = base64.b64decode(base64_str)# 对base64字符串解码成二进制图像代码
    img = skimage.io.imread(imgdata, plugin='imageio')
    cv2.imshow("Login", img)
    print("即将展示二维码，关闭二维码窗口将会自动检查登录")
    cv2.waitKey()
    # 获取用户扫描二维码状态
    url=host+'/login/qr/check'
    data={"key":key}
    response = requests.post(url,data=data)
    re_json=response.json()
    print(re_json)
    if re_json["code"]==803:
        print("登录成功")
        cookie_str=re_json["cookie"]
    else:
        print("登录异常")
        exit() # 退出主程序
    # 返回数据
    return cookie_str
    


# 初始化，检查目录
def init():
     #读取配置文件name，password，cookie
    if not os.path.exists(config_):
        w= open(config_,"w")
        w.write('{}')
        w.close()
    # 创建默认下载目录
    if not os.path.isdir("MusicDownLoad"):
        os.makedirs("MusicDownLoad")  

# 获取歌单详情(包括介绍，名字等等)
def getListDetail(ids,cookie):
    url=host+"/playlist/detail?id="+str(ids)
    response = requests.get(url,headers=header,cookies=cookie)
    json_obj=json.loads(response.text)
    if json_obj["code"]==200:
        j=json_obj["playlist"]
    else:
        print("歌单获取失败，请检查您输入的歌单id")
        sys.exit()
    return j

# 获取歌单所有歌曲id,返回 列表 一系列id
def getListId(j):
    l=[]
    trackIds=j["trackIds"]
    for ids in trackIds :
        #print(ids["id"])
        l.append(ids["id"])
    return l

# 获取音乐真实下载地址
def getMusicUrl(id,cookie):
    url=host+"/song/url?id="+str(id)
    response = requests.get(url,headers=header,cookies=cookie)
    json_obj=json.loads(response.text)
    return json_obj["data"][0]["url"]

# 获取音乐详情（歌名，作者，专辑)
def getMusicDetail(id,cookie):
    url=host+"/song/detail?ids="+str(id)
    response = requests.get(url,headers=header,cookies=cookie)
    json_obj=json.loads(response.text)
    data={}
    if len(json_obj["songs"])>0:
        data["name"]=json_obj["songs"][0]["name"] # 获得歌曲名字
        data["imgUrl"]=json_obj["songs"][0]["al"]["picUrl"]# 获得专辑封面
        # 循环获得作者,拼接字符串
        s=""
        for au in json_obj["songs"][0]["ar"]:
            s+=au["name"]+","
        data["author"]=s
        data["album"]=json_obj["songs"][0]["al"]["name"] # 获得专辑名字
    else:
        pass
    return data

# 打包歌单的歌曲下载链接、歌名等，返回的是json数组对象 # 过程时间比较长，需要进度条
def publishDownLoad(ids,cookie) :
    downl=[]
    
    with tqdm(total=len(ids), desc='进度') as bar:
        t=0
        for i in ids:
            t+=1
            #print("正在处理："+str(i))
            music={}
            music["url"]=getMusicUrl(i,cookie)
            detail=getMusicDetail(i,cookie)
            if detail!={}:
                music["name"]=detail["name"]
                music["author"]=detail["author"]
                music["album"]=detail["album"]
                music["imgUrl"]=detail["imgUrl"]
            else:
                print("歌曲获取失败")
            downl.append(music.copy())
            music.clear()
            bar.update(1)
            
        # 导出下载链接
        file=open("download_link.json","w")
        file.write(json.dumps(downl))
        file.close()
        # bar.update(t+1)
    print("资源整合成功，下载链接已导出,开始下载歌曲")
    return downl

def Download(dl,file):# 由此方法判断选择那种方法下载
    path=""
    if file=="":
        path=os.getcwd()+"\\MusicDownLoad" 
    else:
        path=file
    print(path)
    if input("下载方式选择：0,1（0是选择普通下载;1是IDM下载）")=="1":
        IDMdownload(dl,path)
    else:
        Comdownload(dl,path)

def Comdownload(dl,file):
    print("普通下载中......")
    down_playlist_dir = file+"\\"+ReplaceName(playlistName).strip() # 下载存储位置
    # 建立文件夹
    if os.path.exists(down_playlist_dir):
        pass
    else:
        os.mkdir(down_playlist_dir)
    for info in dl:
        if not info.get("name") or not info.get("url"):
            break
        music_url=info["url"]
        music_name=info["name"]
        down_path=down_playlist_dir+"\\"+ReplaceName(music_name).strip()+".mp3" # 歌曲路径
        try:
            resp=requests.get(music_url,cookies=cookie,headers=header)
            with open(down_path,"wb") as f:
                f.write(resp.content)
            print(f'已完成《{music_name}》歌曲下载')
        except Exception as e:
            print(f"歌曲《{music_name}》下载失败")
    pass

def IDMdownload(dl:list,file:str):# dl参数是列表，每个列表项为字典
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

def ReplaceName(str):
    sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in str:
        if char in sets:
            str = str.replace(char, '')
    return str

if __name__ == '__main__':
    cookie={}          # 全局变量
    playlistName="" # 全局变量
    print("欢迎使用网易云歌单音乐批量导出工具")
    init()
    def l():
            # 是否要登录？
            print("您是否要登录？（非常建议您登录，不登录极大可能出错；而且考虑到安全性，目前仅支持二维码登录）")
            user_input=input("请输入'y'或者'n'（y表示同意登录，n表示不登录）")
            if user_input=='y':
                cook=loginByQR()
                user_json["cookie"]=cook
                # 存储cookie到用户JSON文件
                f=open(config_,"w")
                f.write(json.dumps(user_json))
                f.close()
                # cook=login()# 账号密码登录  #====已废弃，改为二维码登录
            else :
                cookie={}
    # 验证用户JSON文件中的cookie是否可用，不可用就让用户选择是否登录
    with open(config_,"r") as fop:
        config_text=fop.read()
        user_json=json.loads(config_text)
        if "cookie" in user_json.keys():
            # print("有cookie")
            config_cookie=user_json["cookie"]
            cookie=getCookieDict(config_cookie)
            if confirmCookie(cookie):
                print("自动登录成功")
            else:
                l()
        else:
            # print("无cookie")
            l()
        
        
    ids=input("请输入您要下载的歌单id\n\r")
    try:
        play_list=getListDetail(ids=int(ids),cookie=cookie)
        print("歌单名称："+play_list["name"])
        playlistName=play_list["name"]
        print("歌单里歌曲的数量："+str(play_list["trackCount"]))
        musics=getListId(play_list)
        download=publishDownLoad(musics,cookie)
    except :
        print("资源整合出错！")
        print(traceback.format_exc()) 
        sys.exit()
        
    # 下载模块
    if input("是否下载歌曲？（y/n）")=="n":
        sys.exit()
    file_path=input("请输入歌曲保存路径，直接回车，将会保存在默认路径")
    if file_path!="" and os.path.exists(file_path):
        Download(download,file_path)
    elif file_path=="":
        Download(download,"")
    else :
        print("您输入的文件目录不存在,将保存在默认目录下")
        Download(download,"")

    # 退出确认
    while True:
        exit_confirm=input("程序运行结束，输入q退出")
        if exit_confirm=="q":
            exit()
        else :
            continue
