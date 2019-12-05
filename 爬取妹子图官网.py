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
		pxs = random.choice(proxy_list) # 随机选择一个代理
		header = random.choice(my_headers) # 随机选一个浏览器头
		# pxs = {'http': 'http://' + pxs}
		header = {'user-agent':header}
		r = requests.request('GET', url, headers = header)
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

# todo 写注释和修改获取图片链接的逻辑
if __name__ == '__main__':
	url = 'https://www.mzitu.com/all'
	htText = getHTMLText(url)
	soup = BeautifulSoup(htText, 'html.parser')
	count = 0
	totalPictureSets = 200
	pattern = re.compile('https://www.mzitu.com/\d+') # 匹配正确的页面
	mostLiked = ['https://www.mzitu.com/197306',     # 截止11月29号的排行榜的图集网址
	             'https://www.mzitu.com/189574',
	             'https://www.mzitu.com/191199',
	             'https://www.mzitu.com/199289']
	for child in soup.body.descendants:
		if count > totalPictureSets:break
		if child.name == 'a':
			href = child.attrs['href']
			if pattern.match(href):
				# print(child)
				# print(href)
				mostLiked.append(href)
				count += 1
		
	for liked in mostLiked:   # 首先获得所有排行榜中的图片
		html = getHTMLText(liked)
		soup = BeautifulSoup(html, 'html.parser')
		name = liked.split('/')[-1]   # 这个图片集的编号名字
		print('name is', name)
		print(soup.title.contents)    # 也可以用这个title的内容作为图片集编号名字
		matchNofPic = re.compile(liked + '/\d+') # 正则匹配式
		links = [] # 链接列表
		pictures = []
		for child in soup.body.descendants: # 在第一页的源代码里找连续的5个页数标签，
			if child.name == 'img':
				# print('find a picture,', child.attrs['src'])
				pictures.append(child.attrs['src'])
				# getpictureUrl(child.attrs['src'])
			if child.name == 'a':
				# print(child.attrs['href'])
				if matchNofPic.match(child.attrs['href']):
					links.append(child.attrs['href'])
					if len(links) == 5:
						break
		totalPic = links[-1].split('/')[-1]  # 最后那个标签的页码数就是这个图片集的大小
		totalPic = int(totalPic)
		print(liked, 'has total ', totalPic, 'pictures', 'the pictures are:')
		print(pictures[0])
		temp = pictures[0].split('/') # picture这会儿只有第一张图片的网址
		# 将它以‘/’分割后，最后一个字符串就是图片名，对它切片，去掉最后的图片序号加后缀子串
		# 比如'01d01.jpg'去掉后面‘01.jpg’这个子串，就得到图片命名规律的前缀
		temp[-1] = temp[-1][:-6]
		url = '/'.join(temp)
		file = '网址些\\' + name + '.txt'
		if not os.path.exists(file):
			with open(file, 'w') as f:
				f.write(pictures[0] + '\n')
				for i in range(2, totalPic + 1):
					nextpicUrl = url + str(i).zfill(2) + '.jpg' # 用zfill方法填充0-9的情况
					f.write(nextpicUrl + '\n')
					pictures.append(nextpicUrl)
					print(nextpicUrl)
		path = 'I:\爬下的图和视频\\' + name + '\\'  # 存储路径
		if not os.path.exists(path):
			os.mkdir(path)
		else:
			print(name, '该图片集已存在')
			continue
		for pic in pictures:
			print(pic, 'getting it...')
			if downloadPic(pic, path, name):
				print('got it!')
			
			
				
		
	
			
		
	
			
	