#! python3
#-*- coding:utf-8 -*-
'''
   抓取包含某字的诗词，统计作者、数量
   网站: http://www.poeming.com
'''
        
import re
import time
import requests

from collections import Counter


class Poem:  
    name = ''  
    title = ''  
    content = ''

    def __init__(self,n,t,c):
        self.name = n
        self.title = t  
        self.content = c  

def fetch_poetry(baseurl, keyword, poemlist, outfile):
    base_url = baseurl
    bytes_key = keyword.encode('gbk')
    input_str = '%{0:2X}%{1:2X}'.format(bytes_key[0], bytes_key[1])

    # in fisrt page, calc total page num
    page_pattern = re.compile('<A HREF=\'(.*?)\'>(.*?)</A>&nbsp;&nbsp;')
    r = requests.get(base_url + str(1) +'&tp=3&inputword=' + input_str)
    r.encoding='gbk'
    data  = r.text
    page_info = re.findall(page_pattern, data)
    page_num = len(page_info)
    print(page_num)

    # find contain keyword poem
    max_page_num = page_num+1
    poem_pattern = re.compile('<TR><TD>(.*?)</TD><TD>(.*?)</TD><TD>(.*?)</TD></TR>')    
    with open(outfile, 'w', encoding='utf-8') as f:
        for i in range(1, max_page_num):
            print('Downloading page #{}'.format(i))
            r = requests.get(base_url + str(i) +'&tp=3&inputword=' + input_str)
            r.encoding='gbk'
            data = r.text
            p = re.findall(poem_pattern, data)
            for s in p:
                sc = Poem('','','')
                sc.name    = s[0]
                sc.title   = s[1]
                sc.content = "".join(s[2].split()); #去除回车符
                poemlist.append(sc)
                wstr = s[0]+'\t\t'+s[1]+'\t\t\t\t'+s[2]+'\n'
                f.write(wstr)
            time.sleep(2)

def analysis_sc(poemlist, outfile, cntfile):
    nlist=[]
    poemlist.sort(key=lambda sc : sc.name)
    print(len(poemlist))
    
    with open(outfile, 'w', encoding='utf-8') as f:    
        for sc in poemlist:
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

def search_word(word):
    keyword = word

    poemlist=[]
    f1='唐诗_'+keyword+'.txt'
    f2='唐诗_'+keyword+'_s.txt'
    f3='唐诗_'+keyword+'_c.txt'    
    baseurl = "http://www.poeming.com/web/qtssearch.asp?Page="
    fetch_poetry(baseurl, keyword, poemlist, f1)    
    analysis_sc(poemlist, f2, f3)

    poemlist=[]
    f1='宋词_'+keyword+'.txt'
    f2='宋词_'+keyword+'_s.txt'
    f3='宋词_'+keyword+'_c.txt'        
    baseurl = "http://www.poeming.com/web/qscsearch.asp?Page="
    fetch_poetry(baseurl, keyword, poemlist, f1)
    analysis_sc(poemlist, f2, f3)    

if __name__ == "__main__":   
    search_word('菊')
    search_word('志')

    search_word('风')
