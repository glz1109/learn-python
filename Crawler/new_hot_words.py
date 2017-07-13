#! python3
#-*- coding:utf-8 -*-
'''
   from 《用Python玩转数据》- 新闻标题挖掘
'''
        
import re
import time
import requests

import jieba
import jieba.posseg as pseg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from os import path
from collections import Counter
from scipy.misc import imread
from wordcloud import WordCloud

def fetch_sina_news():
    PATTERN  = re.compile('.shtml" target="_blank">(.*?)</a><span>(.*)</span></li>')     
    BASE_URL = "http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_"
    MAX_PAGE_NUM = 11
    
    with open('subjects.txt','w',encoding='utf-8') as f:
        for i in range(1, MAX_PAGE_NUM):
            print('Downloading page #{}'.format(i))
            r = requests.get(BASE_URL + str(i)+'.shtml')
            r.encoding='gb2312'
            data = r.text
            p = re.findall(PATTERN, data)
            for s in p:
                f.write(s[0])
            time.sleep(2)

def extract_words():
    # jieba.load_userdict('custom_dict.txt')
    jieba.add_word('王者荣耀')

    with open('subjects.txt','r',encoding='utf-8') as f:
        news_subjects = f.readlines()
        stop_words = set(line.strip() for line in open('stopwords.txt'))
        newslist = []
        for subject in news_subjects:
            if subject.isspace():
                continue
            # segment words line by line
            # word_list = jieba.cut(subject)            
            # for word in word_list:
            #     print(word)
            #     if not word in stop_words:
            #         newslist.append(word)

            # print(subject)
            word_list = pseg.cut(subject)
            # print(word_list)
            for word, flag in word_list:
                if not word in stop_words and (flag == 'n' or flag == 'nr'):
                    newslist.append(word)

        # newslist.sort()
        # print(newslist)

        # c = Counter(newslist)

        # for word_freq in c.most_common():
        #     word, freq = word_freq
        #     print(word, freq)

        d = path.dirname(__file__)
        mask_image = imread(path.join(d, "mickey.jpg"))
        content = ' '.join(newslist)
        wordcloud = WordCloud(font_path='simhei.ttf', background_color="white",
        mask=mask_image, max_words=40).generate(content)
        
        # Display the generated image:
        plt.imshow(wordcloud)
        plt.axis("off")
        wordcloud.to_file('wordcloud.jpg')
        plt.show()

if __name__ == "__main__":
    fetch_sina_news()
    extract_words()