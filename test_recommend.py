#SnowNLP技术获取评论得分
# -*- coding: utf-8 -*-
from snownlp import SnowNLP
import codecs
import os

ff = open('测试评分结果.txt','w',encoding='UTF-8')
source = open("测试.txt","r",encoding='UTF-8')
line = source.readlines()
sentimentslist = []
for i in line:
    s = SnowNLP(i.encode('utf-8').decode("utf-8","ignore"))
    print(s.sentiments)
    sentimentslist.append(s.sentiments)
    ff.write(str(s.sentiments)+'\n')
sum = 0
for item in sentimentslist:
    sum += item
print("The average score is")
print(sum/len(sentimentslist))
ff.write("平均分为"+'\n')
ff.write(str(sum/len(sentimentslist)))


import matplotlib.pyplot as plt
import numpy as np
# plt.plot(np.arange(0, 1, 1), sentimentslist, 'k-')
plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01))
plt.xlabel('Number')
plt.ylabel('Sentiment')
plt.title('Analysis of Sentiments')
plt.show()

