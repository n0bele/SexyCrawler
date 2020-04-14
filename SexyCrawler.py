#
# author: n0bele@163.com
# date  : 2018/4/2

import requests
import os
import sys
import random
import time
import re
import pymysql
import threading
from lxml import etree
from fake_useragent import UserAgent
pagecount = 10
ua = UserAgent()

def auto49(url,dataname,conn):
    for nPage in range(1,pagecount):
        headers = {"User-Agent":ua.random}
        try:
            mainurl =""
            if(nPage != 1):
                mainurl = url+"recent/"+str(nPage)
            else:
                mainurl = url
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.text)
            for nList in range(0,19):
                try:
                    title = root.xpath('//*[@class="videos"]/li['+str(nList)+']/div/a/@title')
                    watchCount = root.xpath('//*[@class="videos"]/li['+str(nList)+']/div/a/div[2]/span[3]/text()')
                    watchCount = watchCount[0][1:]
                    pic   = root.xpath('//*[@class="videos"]/li['+str(nList)+']/div/a/div/img/@src')
                    findlink = root.xpath('//*[@class="videos"]/li['+str(nList)+']/div/a/@href')
                    sublink = 'http://www.aotu49.com'+findlink[0]
                    headers = {"User-Agent":ua.random}
                    sReuest = requests.Session()
                    subRes = requests.get(sublink,headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    root1 = etree.HTML(subRes.text)
                    mp4link = root1.xpath('//*[@class="video-js vjs-default-skin"]/source[2]/@src')
                    if mp4link[0].strip()!='':
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%s',0,0,0,0)" % (dataname,title[0],pic[0],mp4link[0],watchCount)
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        print sqlexe
                except:
                    info=sys.exc_info()
                    #print info[0],":",info[1]
                    continue
        except:
            continue
    return

def collectionofbestporn(url,dataname,conn):
    for nPage in range(1,pagecount):
        headers = {"User-Agent":ua.random}
        try:
            mainurl = url+"page/"+str(nPage)
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.text)
            for nList in range(2,26):
                try:
                    title = root.xpath('//*[@class="row content-row video-list"]/div['+str(nList)+']/div/div[2]/div/a/@title')
                    watchCount = root.xpath('//*[@class="row content-row video-list"]/div['+str(nList)+']/div/div[2]/div[2]/span[1]/text()')
                    watchCount = re.sub("\D","",watchCount[0])
                    sublink = root.xpath('//*[@class="row content-row video-list"]/div['+str(nList)+']/div/div[1]/a/@href')
                    headers = {"User-Agent":ua.random}
                    sReuest = requests.Session()
                    subRes = sReuest.get(sublink[0],headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    root1 = etree.HTML(subRes.text)
                    pic   = root1.xpath('//*[@id="thisPlayer"]/@poster')
                    mp4link = root1.xpath('//*[@id="thisPlayer"]/source/@src')
                    date  = root1.xpath('//*[@class="item-list"]/li[3]/text()')
                    date = date[0][:10]
                    timeArray = time.strptime(date,"%Y-%m-%d")
                    timestamp = int(time.mktime(timeArray))
                    if mp4link[0].strip()!='':
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%s',0,0,0,'%d')" % (dataname,title[0],pic[0],mp4link[0],watchCount,timestamp)
                        #lock.acquire()
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        #lock.release()
                        print sqlexe
                except:
                    info=sys.exc_info()
                    #print info[0],":",info[1]
                    continue
        except:
            continue
    return

def se2(url,dataname,conn):
    for nPage in range(2,pagecount):
        headers = {"User-Agent":ua.random}
        try:
            mainurl =url+"index-"+str(nPage)+".html"
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.text)
            for nList in range(0,21):
                try:
                    title = root.xpath('//*[@class="vodbox"]/ul/li['+str(nList)+']/a/@title')
                    count = root.xpath('//*[@class="vodbox"]/ul/li['+str(nList)+']/a/em')
                    pic   = root.xpath('//*[@class="vodbox"]/ul/li['+str(nList)+']/a/img/@src')
                    findlink = root.xpath('//*[@class="vodbox"]/ul/li['+str(nList)+']/a/@href')
                    date  = root.xpath('//*[@class="vodbox"]/ul/li['+str(nList)+']/p[2]/text()')
                    timeArray = time.strptime(date[0],"%Y-%m-%d")
                    timestamp = int(time.mktime(timeArray))
                    sublink = 'http://www.se2.co'+findlink[0]
                    headers = {"User-Agent":ua.random}
                    sReuest = requests.Session()
                    subRes = sReuest.get(sublink,headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    subroot = etree.HTML(subRes.text)
                    linkcontext = subroot.xpath('//*[@class="player"]/script[2]/text()')
                    nStart = linkcontext[0].find('f:\'')+len('f:\'')
                    nEnd = linkcontext[0].find('.mp4')+len('.mp4')
                    mp4link = linkcontext[0][nStart:nEnd]
                    ncountLen = len(count[0])-1
                    watchCount = int(count[0].text[2:ncountLen])
                    if (mp4link.strip()!='' and mp4link.find("11bubu.com")==-1):
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%d',0,0,0,'%d')" % (dataname,title[0],pic[0],mp4link,watchCount,timestamp)
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        print sqlexe
                except:
                    continue
        except:
            continue
    return

def www9ppav(url,dataname,conn):
    for nPage in range(2,18):
        headers = {"User-Agent":ua.random}
        try:
            mainurl =url+"index-"+str(nPage)+".html"
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.content)
            for nList in range(1,12):
                try:
                    title = root.xpath('//*[@class="box movie_list"]/ul/li['+str(nList)+']/a/h3/text()')
                    pic   = root.xpath('//*[@class="box movie_list"]/ul/li['+str(nList)+']/a/img/@src')
                    findlink = root.xpath('//*[@class="box movie_list"]/ul/li['+str(nList)+']/a/@href')
                    date  = root.xpath('//*[@class="box movie_list"]/ul/li['+str(nList)+']/a/span/text()')
                    timeArray = time.strptime(date[0],"%Y-%m-%d")
                    timestamp = int(time.mktime(timeArray))
                    sublink = 'https://www.827ww.com'+findlink[0]
                    watchCount = random.randint(8000,90000)
                    headers = {"User-Agent":ua.random}
                    SubReuest = requests.Session()
                    subRes = SubReuest.get(sublink,headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    subroot = etree.HTML(subRes.content)
                    nStart = subRes.content.find('down_url = \'')+len('down_url = \'')
                    sStart = subRes.content[nStart:]
                    sEnd = sStart.find('\'')
                    mp4link = sStart[:sEnd]
                    mp4link = mp4link.replace('https://d.9xxav.com','https://d.eeoai.com')
                    if (mp4link.strip()!=''):
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%d',0,0,0,'%d')" % (dataname,title[0],pic[0],mp4link,watchCount,timestamp)
                        #lock.acquire()
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        #lock.release()
                        print sqlexe
                        
                except:
                    #info=sys.exc_info()
                    #print info[0],":",info[1]
                    continue
        except:
            continue
    return
    
def vipissy(url,dataname,conn):
    for nPage in range(1,15):
        headers = {"User-Agent":ua.random}
        try:
            mainurl =url+str(nPage)
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.content)
            for nList in range(0,20):
                try:
                    title = root.xpath('//*[@class="updates_list"]/div['+str(nList)+']/div//h2/a/text()')
                    pic   = root.xpath('//*[@class="updates_list"]/div['+str(nList)+']/a/img/@src')
                    sublink = root.xpath('//*[@class="updates_list"]/div['+str(nList)+']/a/@href')
                    watchCount = random.randint(2000,30000)
                    headers = {"User-Agent":ua.random}
                    sReuest = requests.Session()
                    subRes = sReuest.get(sublink[0],headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    subroot = etree.HTML(subRes.content)
                    mp4link = subroot.xpath('//*[@id="video"]/source/@src')
                    if (mp4link[0].strip()!=''):
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%d',0,0,0,0)" % (dataname,title[0],pic[0],mp4link[0],watchCount)
                        #lock.acquire()
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        #lock.release()
                        print sqlexe
                except:
                    continue
        except:
            continue
    return

def www84ia(url,dataname,conn):
    for nPage in range(1,pagecount):
        headers = {"User-Agent":ua.random}
        try:
            if nPage == 1:
                mainurl = url+".html"
            else:
                mainurl = url+"_"+str(nPage)+".html"
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.content)
            for nList in range(1,10):
                try:
                    title = root.xpath('//*[@class="text"]/ul/li['+str(nList)+']/div[2]/p/a/text()')
                    title = title[0].encode('raw_unicode_escape').decode('gb2312')
                    findlink = root.xpath('//*[@class="text"]/ul/li['+str(nList)+']/div[2]/p/a/@href')
                    sublink = 'http://www.84ia.com'+findlink[0]
                    pic = root.xpath('//*[@class="text"]/ul/li['+str(nList)+']/div/a/img/@src')
                    date  = root.xpath('//*[@class="text"]/ul/li['+str(nList)+']/div[2]/p[4]/text()')
                    date = date[0][10:]
                    timeArray = time.strptime(date,"%Y-%m-%d")
                    timestamp = int(time.mktime(timeArray))
                    watchCount = random.randint(2000,30000)
                    headers = {"User-Agent":ua.random}
                    sReuest = requests.Session()
                    subRes = sReuest.get(sublink,headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    subroot = etree.HTML(subRes.content)
                    nStart = subRes.content.find('f:\'')+len('f:\'')
                    sStart = subRes.content[nStart:]
                    sEnd = sStart.find('\'')
                    mp4link = sStart[:sEnd]
                    if mp4link.strip()!='':
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%d',0,0,0,%d)" % (dataname,title,pic[0],mp4link,watchCount,timestamp)
                        #lock.acquire()
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        #lock.release()
                        print sqlexe
                except:
                    info=sys.exc_info()
                    print info[0],":",info[1],":line",info[2].tb_lineno
                    continue
        except:
            continue
    return

def xvideos(url,dataname,conn):
    for nPage in range(0,pagecount):
        headers = {"User-Agent":ua.random}
        try:
            if nPage == 0:
                mainurl = url
            else:
                mainurl = url+str(nPage)
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.content)
            for nList in range(1,25):
                try:
                    title = root.xpath('//*[@class="mozaique"]/div['+str(nList)+']/div[2]/p/a/@title')
                    title = title[0].encode('raw_unicode_escape')
                    findlink = root.xpath('//*[@class="mozaique"]/div['+str(nList)+']/div[2]/p/a/@href')
                    sublink = 'https://www.xvideos.com'+findlink[0]
                    pic = root.xpath('//*[@class="mozaique"]/div['+str(nList)+']/div/div/a/img/@data-src')
                    headers = {"User-Agent":ua.random}
                    sReuest = requests.Session()
                    subRes = sReuest.get(sublink,headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    subroot = etree.HTML(subRes.content)
                    watchCount = subroot.xpath('//*[@id="video-views-votes"]/span/span/strong/text()')
                    watchCount = re.sub("\D","",watchCount[0])
                    nStart = subRes.content.find('setVideoUrlLow(\'')+len('setVideoUrlLow(\'')
                    sStart = subRes.content[nStart:]
                    sEnd = sStart.find('\')')
                    mp4link = sStart[:sEnd]
                    if mp4link.strip()!='':
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%s',0,0,0,0)" % (dataname,title,pic[0],mp4link,watchCount)
                        #lock.acquire()
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        #lock.release()
                        print sqlexe
                except:
                    info=sys.exc_info()
                    print info[0],":",info[1],":line",info[2].tb_lineno
                    continue
        except:
            continue
    return

def pornhub(url,dataname,conn,page):
    for nPage in range(1,page):
        headers = {"User-Agent":ua.random}
        try:
            mainurl = url+str(nPage)
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.content)
            for nList in range(1,25):
                try:
                    title = root.xpath('//*[@id="videoSearchResult"]/li['+str(nList)+']/div/div[3]/span/a/@title')
                    #watchCount = root.xpath('//*[@id="videoSearchResult"]/li['+str(nList)+']/div/div[3]/div/span/var/text()')
                    #watchCount = int(watchCount[0][0:len(watchCount[0])-1])*1000
                    watchCount = random.randint(20000,300000)
                    findlink = root.xpath('//*[@id="videoSearchResult"]/li['+str(nList)+']/div/div[3]/span/a/@href')
                    sublink = 'https://www.pornhub.com'+findlink[0]
                    pic = root.xpath('//*[@id="videoSearchResult"]/li['+str(nList)+']/div/div/div[2]/a/img/@data-thumb_url')
                    headers = {"User-Agent":ua.random}
                    sReuest = requests.Session()
                    subRes = sReuest.get(sublink,headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    subroot = etree.HTML(subRes.content)
                    nStart = subRes.content.find('240","videoUrl":"')+len('240","videoUrl":"')
                    sStart = subRes.content[nStart:]
                    sEnd = sStart.find('"')
                    mp4link = sStart[:sEnd]
                    mp4link = mp4link.replace("\/", "/")
                    if mp4link.find('mp4?ttl=') == -1:
                        continue
                    if mp4link.strip()!='':
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%d',0,0,0,0)" % (dataname,title[0],pic[0],mp4link,watchCount)
                        #lock.acquire()
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        #lock.release()
                        print sqlexe
                except:
                    info=sys.exc_info()
                    print info[0],":",info[1],":line",info[2].tb_lineno
                    continue
        except:
            continue
    return

def porn(url,dataname,conn):
    for nPage in range(1,pagecount):
        headers = {"User-Agent":ua.random}
        try:
            mainurl = url+str(nPage)
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.content)
            for nList in range(2,42):
                try:
                    title = root.xpath('//*[@class="thumb-list videos"]/div['+str(nList)+']/h3/a/@title')
                    watchCount = root.xpath('//*[@class="thumb-list videos"]/div['+str(nList)+']/div[2]/p[2]/text()')
                    watchCount = int(watchCount[0][0:len(watchCount[0])-7])*1000
                    pic = root.xpath('//*[@class="thumb-list videos"]/div['+str(nList)+']/div/a/img[1]/@src')
                    findid = root.xpath('//*[@class="thumb-list videos"]/div['+str(nList)+']/div/a/@href')
                    nStart = findid[0].rfind('-')+1
                    mp4link = 'https://www.porn.com/download/240/'+findid[0][nStart:]+'.mp4'
                    if mp4link.strip()!='':
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%d',0,0,0,0)" % (dataname,title[0],pic[0],mp4link,watchCount)
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        print sqlexe
                except:
                    continue
        except:
            continue
    return

def xhamster(url,dataname,conn):
    for nPage in range(1,6):
        headers = {"User-Agent":ua.random}
        try:
            mainurl = url+str(nPage)
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.content)
            for nList in range(1,61):
                try:
                    title = root.xpath('//*[@class="thumb-list thumb-list--margin thumb-list--sidebar thumb-list--banner"]/div['+str(nList)+']/a/img/@alt')
                    watchCount = root.xpath('//*[@class="thumb-list thumb-list--margin thumb-list--sidebar thumb-list--banner"]/div['+str(nList)+']/div/i[1]/text()')
                    watchCount = re.sub("\D","",watchCount[0])
                    sublink = root.xpath('//*[@class="thumb-list thumb-list--margin thumb-list--sidebar thumb-list--banner"]/div['+str(nList)+']/a/@href')
                    pic = root.xpath('//*[@class="thumb-list thumb-list--margin thumb-list--sidebar thumb-list--banner"]/div['+str(nList)+']/a/img/@src')
                    sReuest = requests.Session()
                    headers = {"User-Agent":ua.random}
                    subRes = sReuest.get(sublink[0],headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    subroot = etree.HTML(subRes.content)
                    nStart = subRes.content.find('"240p":"')+len('"240p":"')
                    sStart = subRes.content[nStart:]
                    sEnd = sStart.find('"')
                    mp4link = sStart[:sEnd]
                    mp4link = mp4link.replace("\/", "/")
                    date  = subroot.xpath('//*[@class="entity-container__block entity-info-container entity-info-container--titled"]/div[3]/@content')
                    timeArray = time.strptime(date[0],"%Y-%m-%d")
                    timestamp = int(time.mktime(timeArray))
                    if mp4link.strip()!='':
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%s',0,0,0,'%d')" % (dataname,title[0],pic[0],mp4link,watchCount,timestamp)
                        #lock.acquire()
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        #lock.release()
                        print sqlexe
                except:
                    info=sys.exc_info()
                    #print info[0],":",info[1]
                    continue
        except:
            continue
    return

def redtube(url,dataname,conn):
    for nPage in range(1,pagecount):
        headers = {"User-Agent":ua.random}
        try:
            mainurl = url+str(nPage)
            sReuest = requests.Session()
            mainRes = sReuest.get(mainurl,headers=headers,timeout=(3,7))
            mainRes.encoding='utf-8'
            root = etree.HTML(mainRes.content)
            for nList in range(1,38):
                try:
                    title = root.xpath('//*[@id="content_container"]/div[2]/ul/li['+str(nList)+']/div/span/a/img/@alt')
                    pic = root.xpath('//*[@id="content_container"]/div[2]/ul/li['+str(nList)+']/div/span/a/img/@src')
                    watchCount = root.xpath('//*[@id="content_container"]/div[2]/ul/li['+str(nList)+']/div/span[2]/text()')
                    sublink = root.xpath('//*[@id="content_container"]/div[2]/ul/li['+str(nList)+']/div/span/a/@href')
                    #title = root.xpath('//*[@id="content_container"]/ul/li['+str(nList)+']/div/div/div/a/@title')
                    #pic = root.xpath('//*[@id="content_container"]//ul/li['+str(nList)+']/div/div/span/a/img/@src')
                    #watchCount = root.xpath('//*[@id="content_container"]/ul/li['+str(nList)+']/div/span[1]/text()')
                    watchCount = re.sub("\D","",watchCount[0])
                    #sublink = root.xpath('//*[@id="content_container"]/ul/li['+str(nList)+']/div/div/span/a/@href')
                    sublink = 'https://www.redtube.com'+sublink[0]
                    sReuest = requests.Session()
                    headers = {"User-Agent":ua.random}
                    subRes = sReuest.get(sublink,headers=headers,timeout=(3,7))
                    subRes.encoding='utf-8'
                    subroot = etree.HTML(subRes.content)
                    nStart = subRes.content.find('"240","videoUrl":"')+len('"240","videoUrl":"')
                    sStart = subRes.content[nStart:]
                    sEnd = sStart.find('"')
                    mp4link = sStart[:sEnd]
                    mp4link = mp4link.replace("\/", "/")
                    if mp4link.strip()!='':
                        sqlexe ="REPLACE INTO %s(title,pic,playUrl,watchCount,collectionCount,shareCount,replyCount,date) VALUES('%s','%s','%s','%s',0,0,0,0)" % (dataname,title[0],pic[0],mp4link,watchCount)
                        #lock.acquire()
                        cursor = conn.cursor()
                        cursor.execute(sqlexe)
                        conn.commit()
                        cursor.close()
                        #lock.release()
                        print sqlexe
                except:
                    continue
        except:
            continue

if __name__ == "__main__":
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='chengye',charset = 'utf8')
    while 1:
        #www9ppav("https://www.827ww.com/Html/101/","hdongman",conn,lock)
        #redtube("https://www.redtube.com/redtube/japanese?page=","renqishunv",conn)
        xhamster("https://xhamster.com/search?q=blonde&p=","oumeiav",conn)
        pornhub("https://www.pornhub.com/video/search?search=lesbian&page=","lesbian",conn,30)
        vipissy("https://www.vipissy.com/updates/page-","hdvideo",conn)
        collectionofbestporn("http://collectionofbestporn.com/category/japanese/","renqishunv",conn)
        xvideos("https://www.xvideos.com/?k=%e7%a0%b4%e5%a4%84&p=","virgin",conn)
        xhamster("https://xhamster.com/search?q=feet&p=","feet",conn)
        pornhub("https://www.pornhub.com/video/search?search=%E6%99%BA%E8%83%BD%E6%8D%A2%E8%84%B8&page=","ai",conn,2)
        collectionofbestporn("http://collectionofbestporn.com/category/threesome/","3pvideo",conn)
        xvideos("https://www.xvideos.com/?k=%e4%ba%ba%e5%85%bd&p=","renshou",conn)
        time.sleep(10)
    conn.close()
    print "DONE"

