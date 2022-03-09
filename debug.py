import requests
import re
import os
from bs4 import BeautifulSoup


# 创建文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  " + path)
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")


# 本地存放地址
file = "d:\\trngish\\debug"
# #获取图片   输入网址
url = "https://www.tuiimg.com/meinv/"
isWhile = True
i = 943
while isWhile:
    imgUrl = url + str(i) + "/"
    i = i + 1
    try:
        req = requests.get(imgUrl)
        html = req.text
        title = re.findall('<title>(.*)</title>', html)[0]
        if "妲己" not in title:
            if "心妍" not in title:
                continue
        # 使用beautifulSoup接受这个html
        soup = BeautifulSoup(html, "html.parser")
        # 找到图片地址
        link = soup.find("img", id="nowimg").get("src")
        # 替换掉完整地址，后面循环拼接成完整地址
        link = re.sub(r'1.jpg', "", link)
        # 根据标题生成文件夹
        imgFile = file + "\\" + title
        mkdir(imgFile)
        flag = True
        count = 1
        while flag:
            # 拼接成完整地址
            src = link + str(count) + ".jpg"
            # 请求src的路径
            req = requests.get(src)
            if req.status_code == 200:  # 如果当前地址不存在，则说明当前组图片已全部下载，退出当前拼接地址循环
                # 在这里传入你想保存的文件夹
                with open(imgFile + "/" + str(count) + '.jpg', 'wb') as f:
                    # req.content就是获取src的内容，就是他的图片
                    f.write(req.content)
                count = count + 1
            else:
                print(title + " 下载：" + str(count - 1) + "张")
                flag = False
    except BaseException:  # 只要出异常，都能出循环结束进程
        print("已下载组数：" + str(i - 1))
        isWhile = False
