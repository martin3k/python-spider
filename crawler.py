# encoding=utf-8
'''
@author:   pip install zjj =_=
@software: Pycharm
@time:     2019/11/29 20:16
@filename: 爬取妹子图官网.py
@contact:  1326632773@qq.com
'''
from bs4 import BeautifulSoup
import re
import os
import requests
import random
from getGraph import getGraph

# 第一步，从每日更新页面获取所有妹子图的链接
# 第二步，进入每个链接，把该链接下的所有图片下载下来
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
proxy_list = [
    '27.152.91.95:9999',
    '112.87.70.176:9999',
    '183.166.118.242:9999',
    '120.83.103.139:9999'
]


def getHTMLText(url):
    try:
        pxs = random.choice(proxy_list)  # 随机选择一个代理
        header = random.choice(my_headers)  # 随机选一个浏览器头
        # pxs = {'http': 'http://' + pxs}
        header = {'user-agent': header}
        r = requests.request('GET', url, headers=header)
        # print(r.status_code)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('Failed')
        exit(-1)


def getpictureUrl(soup):
    for child in soup.body.descendants:  # 在第一页的源代码里找连续的5个页数标签，
        if child.name == 'img':
            # print('find a picture,', child.attrs['src'])
            return child.attrs['src']


def downloadPic(url, root, name):
    getGraph(url, root, name)
    return True


def getFromURL(url):
    htText = getHTMLText(url)
    soup = BeautifulSoup(htText, 'html.parser')
    count = 0
    totalPictureSets = 200
    pattern = re.compile('https://www.dma96.com/tupian/\d+')  # 匹配正确的页面
    mostLiked = []
    for item in soup.find_all("a"):
        href = 'https://www.dma96.com' + str(item.get("href"))
        if pattern.match(href):
            print(href)
            mostLiked.append(href)
    for liked in mostLiked:  # 首先获得所有排行榜中的图片

        html = getHTMLText(liked)
        soup = BeautifulSoup(html, 'html.parser')
        name = liked.split('/')[-1]  # 这个图片集的编号名字

        print('name is', name)
        print(soup.title.contents)  # 也可以用这个title的内容作为图片集编号名字

        pattern = re.compile('https://mmtp1.com/maomao/yazhou/\d+')  # 匹配正确的页面
        href = str(item.get("href"))
        pictures = []
        for item in soup.find_all("img"):
            link = item.get("data-original")
            print(link)
            pictures.append(link)

        totalPic = len(pictures)
        print('has total ', totalPic, 'pictures')

        file = '/users/sunny/martin/爬下的图和视频/' + name + '.txt'
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write(pictures[0] + '\n')
                for i in range(2, totalPic + 1):
                    nextpicUrl = url + str(i).zfill(2) + '.jpg'  # 用zfill方法填充0-9的情况
                    f.write(nextpicUrl + '\n')
                    pictures.append(nextpicUrl)
                    print(nextpicUrl)
        path = '/users/sunny/martin/爬下的图和视频/' + name + '/'  # 存储路径
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            print(name, '该图片集已存在')
            continue
        for pic in pictures:
            print(pic, 'getting it...')
            if downloadPic(pic, path, name):
                print('got it!')


# todo 写注释和修改获取图片链接的逻辑
if __name__ == '__main__':
    urlList = []
    for i in range(1, 150):
        url = 'https://www.dma96.com/tupian/list-欧美色图-' + str(i) + '.html'
        urlList.append(url)
        url = 'https://www.dma96.com/tupian/list-清纯唯美-' + str(i) + '.html'
        urlList.append(url)
        url = 'https://www.dma96.com/tupian/list-亚洲色图-'+str(i)+'.html'
        urlList.append(url)
    for url in urlList:
        getFromURL(url)









