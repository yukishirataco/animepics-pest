# -*- coding:utf-8 -*-
'''
Python爬虫 for Gelbooru
作者:Yukino Shiratama
基于https://github.com/KaitoKid/EcchiBot提供的Gelbooru API图片获取代码
'''
import time
import requests
from bs4 import BeautifulSoup
from urllib import request
import os
import re
import random
inputs = input('请输入你要查询的tag(可以有多个)')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'} 
r = requests.get(r'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=rating%3asafe '+inputs,headers=headers) 
#以伪装的Header爬取Gelbooru相关tag内容
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "lxml")
    #如果API页面能正常打开
    num = int(soup.find('posts')['count'])
    #就用bs4解析网页
    maxpage = int(round(num/100))
    #查看页面上有多少图片，以100张图一页的话有多少图
    count=0
    print('Gelbooru API访问正常...\n对于tag:'+inputs+' rating:safe,有'+str(num)+'张图，'+str(maxpage)+'页')
    if num == 0:
        print('没有找到图片，可能是出错了...')
        #找到所有的图片
        #如果没有图片就说明出问题了
    else:
        for page in range(0,maxpage):
        #爬取所有页面的图，所以在每一页都要找到图片
            pgs=requests.get(r'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='+inputs+' rating:safe&pid='+str(page))
            if pgs.status_code == 200:
                getcha=BeautifulSoup(pgs.text,"lxml")
                posts=getcha.find('posts')
                pics=posts.find_all('post')
                for link in pics:
                    request.urlretrieve(link['file_url'], r'%s' % link['file_url'][40:])
                    count=count+1
                    #图片计数加一
                    print('已成功下载'+link['file_url'][40:]+',共'+str(num)+'张图,还剩'+str(num-count)+'张,现在位于第'+str(page)+'页')
                print('第'+str(page)+'页已经爬取完毕，下一页是'+str(page+1))
