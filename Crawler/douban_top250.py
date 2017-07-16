#! python3
# coding=utf-8

import requests
from bs4 import BeautifulSoup
import time
import re


def getmovielist(murl, baseurl, movielist):
    time.sleep(2)
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    print(murl)            
    res  = requests.get(murl)
    soup = BeautifulSoup(res.text, 'html.parser')
    movielistsinfo = soup.select('.grid_view li')
    for m in movielistsinfo:
        rank     = m.select('em')[0].text
        title    = m.select('.title')[0].text
        direct   = m.select('.info .bd p')[0].text.strip()
        rate     = m.select('.rating_num')[0].text.strip()

        # print(direct)
        fields   = direct.split('\n')        
        staff    = fields[0].split('主演:')

        director = staff[0].strip()
        director = director.replace(': ', ':\t')

        if len(staff) > 1:
            starring = '主演:\t' + staff[1].strip()
        else:
            starring = ' '

        info = fields[1].split('/')
        date     = info[0].strip()
        country  = info[1].strip()
        style    = info[2].strip()

        if m.select('.inq'):
            comments = m.select('.inq')[0].text.strip()
        else:
            comments = 'None'
        movielist.append('排名:\t'+ rank+ '\n' + \
                '片名:\t'+ title + '\n'+ \
                director + '\n' + \
                starring + '\n' + \
                '上映日期: '+ date + '\n'+ \
                '国家地区: '+ date + '\n'+ \
                '类型:\t'+ style + '\n'+ \
                '评论:\t'+ comments +'\n' + \
                '豆瓣评分: '+ rate + '\n'+ '\n')
    if soup.select('.next a'):
        asoup = soup.select('.next a')[0]['href']
        next_page = baseurl + asoup
        getmovielist(next_page, baseurl, movielist)
    else:
        print('END')

def getbooklist(burl, booklist):
    time.sleep(2)
    print(burl)            
    res  = requests.get(burl)
    soup = BeautifulSoup(res.text, 'html.parser')
    booklistsinfo = soup.select('.indent table')
    for book in booklistsinfo:
        title = book.select('.pl2 a')[0].text.strip()
        title = "".join(title.split())   #去除str中间的空格、回车符、跳表符
        author= book.select('.pl')[0].text.strip()
        
        fields= author.split('/')
        num = len(fields)
        price = fields[num-1].strip()
        date  = fields[num-2].strip()
        publisher = fields[num-3].strip()
        if num> 4:
            author = fields[0].strip() + ' / ' + fields[1].strip()
        else:
            author = fields[0].strip()

        if book.select('.inq'):
            comments = book.select('.inq')[0].text.strip()
        else:
            comments = 'None'

        rate = book.select('.rating_nums')[0].text.strip()

        booklist.append('书名:\t'+ title + '\n' + '作者:\t' + author + '\n' + \
            '出版社:\t' + publisher + '\n' + \
            '出版年:\t' + date + '\n' + \
            '定价:\t' + price + '\n' + \
            '评论:\t'+ comments +'\n' + 
            '豆瓣评分: '+ rate +'\n' + '\n')
    
    if soup.select('.next a'):
        asoup = soup.select('.next a')[0]['href']
        next_page = asoup
        getbooklist(next_page, booklist)
    else:
        print('END')        


if __name__ == '__main__':
    murl = 'https://movie.douban.com/top250'
    baseurl = 'https://movie.douban.com/top250'
    movielist = []

    getmovielist(murl, baseurl, movielist)    

    with open('douban_movie_top250.txt', 'w', encoding='utf-8') as f:
        for m in movielist:
            f.write(m)

    burl = 'https://book.douban.com/top250'
    booklist = []

    getbooklist(burl, booklist)    

    with open('douban_book_top250.txt', 'w', encoding='utf-8') as f:
        for b in booklist:
            f.write(b)    