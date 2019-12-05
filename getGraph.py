# encoding=utf-8
'''
@author:   pip install zjj =_=
@software: Pycharm
@time:     2019/9/29 17:34
@filename: getGraph.py
@contack:  1326632773@qq.com
'''
import requests
import os
import openpyxl

def getGraph(url, root, name):
	# print(url.split('/')[-2])
	# print(url.split('/')[-1])
	filename = url.split('/')[-2] + '-' + url.split('/')[-1]
	# print(filename)
	path = root + filename
	print(path)
	try:
		if not os.path.exists(root):
			os.mkdir(root)
		
		if not os.path.exists(path):
			print('getting the web page...')
			headers = {
				'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
				'Connection': 'Keep-Alive',
				'Referer'   : "http://www.mzitu.com/" + name
			}
			r = requests.get(url, headers = headers, timeout = 20)
			r.raise_for_status()
			print(r.status_code)
			print('got it')
			f = open(path, 'wb')
			f.write(r.content)
			f.close()
			print("file " + filename + " save succeed")
			# with open (path, 'wb') as f:
			# 	f.write(r.content)
			# 	f.close()
			# 	print("file " + filename + " save succeed")
		else :
			print("file " + filename + " already exist")
	except:
		print("爬取失败")
		
# #进一步，还能爬视频，音频等
# url = 'https://i5.meizitu.net/2017/02/26a01.jpg'
# root = 'D://'
# r = requests.get(url, timeout = 20)
# getGraph(url, root)
#爬取崩坏3官网上的壁纸
# for i in range(1, 37):
# 	num = '0' + str(i) if i < 10 else str(i)
# 	url =
# 	getGraph(url)
