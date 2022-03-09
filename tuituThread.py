import sys
import threading
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


class myThread(threading.Thread):
    def __init__(self, threadID, name, begin, end, url):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.begin = begin
        self.end = end
        self.url = url

    def run(self):
        print("开始线程：" + self.name)
        downloadTuiTu(self.begin, self.end, self.url, self.name)
        print("退出线程：" + self.name)


# 下载推图网照片
def downloadTuiTu(begin, end, url, threadName):
    for i in range(begin, end):
        imgUrl = url + str(i) + "/"
        i = i + 1
        try:
            req = requests.get(imgUrl)
            html = req.text
            title = re.findall('<title>(.*)</title>', html)[0]
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
                    print(title + " 下载：" + str(count - 1) + "张。" + threadName)
                    flag = False
        except BaseException:  # 只要出异常，都能出循环结束进程
            print(threadName + "组，" + "已下载组数：" + str(i - 1 - begin))
            break


# 本地存放地址
file = "d:\\trngish\\tuitu"
# #获取图片   输入网址
url = "https://www.tuiimg.com/meinv/"

total = 2436  # 总组数
one = 100  # 每一百组一个线程
try:
    thread_list = []
    count = 1
    for i in range(int(total // one + 1)):
        # 创建新线程
        thread_list.append(myThread(i, "Thread-" + str(i), count, count + one, url))
        count = count + one + 1
    # 开启新线程
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    print("主线程退出")
except:
    print("Error: 无法启动线程")
    print(sys.exc_info()[0])
    raise
