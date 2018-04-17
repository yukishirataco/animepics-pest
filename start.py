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
input(‘请输入你要查询的tag(可以有多个)')
r = requests.get(r'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=rating%3asafe'+inputs,headers=headers) 
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'} 
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "lxml")
    num = int(soup.find('posts')['count'])
    maxpage = int(round(num/100))
    #if there are less than 100 posts, stay on page 0
    page = random.randint(0, maxpage)
    #make the soup and get all posts
    t = soup.find('posts')
    p = t.find_all('post')
    #if there are no posts, something is wrong
    if num == 0:
        msg = 'something wrong'
    else:
        for i in range(0,num):
            # only one page cus <100 results
            if num < 100:
                pic = p[i]
            elif page == maxpage:
                pic = p[i]
            else:
                pic = p[i]
            print(pic['file_url'])
            request.urlretrieve(pic['file_url'], r'F:\pest\%s.jpg' % pic['file_url'][40:-4])

