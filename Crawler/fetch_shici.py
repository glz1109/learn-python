#! python3
#-*- coding:utf-8 -*-
'''
   抓取包含某字的诗词，统计作者、数量
   网站: http://www.poeming.com
'''
        
import re
import time
import requests

# import jieba
# import jieba.posseg as pseg
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# from os import path
from collections import Counter
# from scipy.misc import imread
# from wordcloud import WordCloud

class ShiCi:  
    name = ''  
    title = ''  
    content = ''

    def __init__(self,n,t,c):
        self.name = n
        self.title = t  
        self.content = c  

def fetch_shici(baseurl, keyword, pagenum, sclist, outfile):
    PATTERN  = re.compile('<TR><TD>(.*?)</TD><TD>(.*?)</TD><TD>(.*?)</TD></TR>')
    BASE_URL = baseurl
    MAX_PAGE_NUM = pagenum+1
    
    bytes_key = keyword.encode('gbk')
    input_str = '%{0:2X}%{1:2X}'.format(bytes_key[0], bytes_key[1])

    with open(outfile, 'w', encoding='utf-8') as f:
        for i in range(1, MAX_PAGE_NUM):
            print('Downloading page #{}'.format(i))
            r = requests.get(BASE_URL + str(i) +'&tp=3&inputword=' + input_str)
            r.encoding='gbk'
            data = r.text
            p = re.findall(PATTERN, data)
            for s in p:
                sc = ShiCi('','','')
                sc.name    = s[0]
                sc.title   = s[1]
                sc.content = "".join(s[2].split()); #去除回车符
                sclist.append(sc)
                wstr = s[0]+'\t\t'+s[1]+'\t\t\t\t'+s[2]+'\n'
                f.write(wstr)
            time.sleep(2)

def analysis_sc(sclist, outfile, cntfile):
    nlist=[]
    sclist.sort(key=lambda sc : sc.name)
    print(len(sclist))
    
    with open(outfile, 'w', encoding='utf-8') as f:    
        for sc in sclist:
            # print(sc.name)
            nlist.append(sc.name)
            wstr = '{0:s}\t\t{1:s}\t\t{2:s}\n'.format(sc.name, sc.title, sc.content)
            f.write(wstr)
        
    c = Counter(nlist)
    with open(cntfile, 'w', encoding='utf-8') as f:    
        for name_freq in c.most_common():
            name, freq = name_freq
            print(name, freq)
            cstr='{0:s}\t{1:d}\n'.format(name, freq)
            f.write(cstr)

if __name__ == "__main__":   
    keyword = '菊'

    sclist=[]
    baseurl = "http://www.poeming.com/web/qtssearch.asp?Page="
    fetch_shici(baseurl, keyword, 23, sclist, 'tanshi_ju.txt')
    analysis_sc(sclist, 'tanshi_ju_sort.txt', 'count_ts_ju.txt')

    sclist=[]
    baseurl = "http://www.poeming.com/web/qscsearch.asp?Page="
    fetch_shici(baseurl, keyword, 23, sclist, 'songci_ju.txt')
    analysis_sc(sclist, 'songci_ju_sort.txt', 'count_sc_ju.txt')    

    keyword = '志'

    sclist=[]
    baseurl = "http://www.poeming.com/web/qtssearch.asp?Page="
    fetch_shici(baseurl, keyword, 25, sclist, 'tanshi_zhi.txt')
    analysis_sc(sclist, 'tanshi_zhi_sort.txt', 'count_ts_zhi.txt')

    sclist=[]
    baseurl = "http://www.poeming.com/web/qscsearch.asp?Page="
    fetch_shici(baseurl, keyword, 7, sclist, 'songci_zhi.txt')
    analysis_sc(sclist, 'songci_zhi_sort.txt', 'count_sc_zhi.txt')        