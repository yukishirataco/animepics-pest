# -*- coding:utf-8 -*-
'''
Python爬虫 for Gelbooru
作者:Yukino Shiratama
基于https://github.com/KaitoKid/EcchiBot提供的Gelbooru API图片获取代码
'''
import time
import requests
from bs4 import BeautifulSoup
import urllib.request
import os

def recu_down(url,filename): # recurrent download with ContentTooShortError
    try:
        urllib.request.urlretrieve(url,filename)
    except urllib.error.ContentTooShortError:
        print ('Network conditions is not good. Reloading...')
        recu_down(url,filename)
        
if os.path.exists('./downloads'):
    #下载目录存在，什么都不做
    pass
else:
    print("下载目录不存在...建立中...")
    os.makedirs('./downloads')
print('Anime Pest')
inputs = input('请输入你要查询的tag(可以有多个):')
#选择图片来源
src_i = input('请输入图片来源，1.Gelbooru,2.Yande.re(默认为Gelbooru):')
if src_i == '1':
    source = r'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='
elif src_i == '2':
    source = r'https://yande.re/post.xml?tags='
else:
    source = r'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='
    src_i='1'
#选择图片分级
rate_i = input('请输入图片分级，1.safe，2.questionable和safe，3.explicit+safe+questionable，(默认为safe):')
if rate_i == '1':
    rate=' rating:safe'
elif rate_i == '2':
    rate=' -rating:explicit'
else:
    rate=' '

compress = input('是否需要压缩成zip文件（会自动删除源文件）?(y/N,默认:N)')
if compress == 'y' or 'Y':
    zipped = True
elif compress == 'n' or 'N':
    zipped = False
else:
    zipped = False

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'} 
r = requests.get(source+inputs+rate+' -comic -monochrome',headers=headers) 
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

#以伪装的Header爬取Gelbooru相关tag内容
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "lxml")
    #如果API页面能正常打开
    num = int(soup.find('posts')['count'])
    #就用bs4解析网页
    maxpage = int(round(num/100))
    #查看页面上有多少图片，以100张图一页的话有多少图
    count=0
    print('API访问正常...\n对于tag:'+inputs+rate+',有'+str(num)+'张图，'+str(maxpage)+'页')
    if num == 0:
        print('没有找到图片，可能是出错了...')
        #找到所有的图片
        #如果没有图片就说明出问题了
    else:
        for page in range(0,maxpage+1):
        #爬取所有页面的图，所以在每一页都要找到图片
            if src_i == '1':
                pgs=requests.get(source+inputs+rate+'&pid='+str(page))
            elif src_i == '2':
                pgs=requests.get(source+inputs+rate+'&page='+str(page))
            if pgs.status_code == 200:
                getcha=BeautifulSoup(pgs.text,"lxml")
                posts=getcha.find('posts')
                pics=posts.find_all('post')
                for link in pics:
                #不同网站使用不同爬取规则
                    if src_i == '1':
                        recu_down(link['file_url'], r'./downloads/%s' % link['file_url'][40:])
                        count=count+1
                        print('已成功下载'+link['file_url'][40:]+',共'+str(num)+'张图,还剩'+str(num-count)+'张,现在位于第'+str(page)+'页')
                    elif src_i == '2':
                        recu_down(link['file_url'], r'./downloads/%s' % link['file_url'][62:])
                        count=count+1
                        print('已成功下载'+link['file_url'][62:]+',共'+str(num)+'张图,还剩'+str(num-count)+'张,现在位于第'+str(page)+'页')
                    #图片计数加一
                if page+1 == maxpage:
                    print('第'+str(page)+'页已经爬取完毕，爬取完成，共获取了'+str(count)+'张图')
                else:
                    print('第'+str(page)+'页已经爬取完毕，下一页是第'+str(page+1)+'页')
            if zipped == True: 
                compress_cmd = 'zip -r '+ 'downloads.zip ' + './downloads/'
                os.system(compress_cmd)
                remove_cmd = 'rm -rf ./downloads'
                os.system(remove_cmd)

