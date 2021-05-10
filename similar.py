import math
import jieba
import numpy as np
from math import sqrt
import csv


# 关键词统计和词频统计，以列表形式返回
def Count(resfile):
    file = open(resfile, "r", encoding='utf-8')  # 此处需打开txt格式且编码为UTF-8的文本
    txt = file.read()
    words = jieba.lcut(txt)  # 使用jieba进行分词，将文本分成词语列表

    count = {}
    for word in words:  # 使用 for 循环遍历每个词语并统计个数
        if len(word) < 2:  # 排除单个字的干扰，使得输出结果为词语
            continue
        else:
            count[word] = count.get(word, 0) + 1  # 如果字典里键为 word 的值存在，则返回键的值并加一，如果不存在键word，则返回0再加上1

    exclude = ["电影", "一起", "这样","一个","还是","没有","因为","那么","可以","有点","非常","就是","觉得","这个","喜欢","什么","自己","第一部"]  # 建立无关词语列表
    for key in list(count.keys()):  # 遍历字典的所有键，即所有word
        if key in exclude:
            del count[key]  # 删除字典中键为无关词语的键值对

    list1 = list(count.items())  # 将字典的所有键值对转化为列表
    list1.sort(key=lambda x: x[1], reverse=True)
    return list1



def MergeWord(T1, T2):
    MergeWord = []
    duplicateWord = 0
    for ch in range(len(T1)):
        MergeWord.append(T1[ch][0])
    for ch in range(len(T2)):
        if T2[ch][0] in MergeWord:
            duplicateWord = duplicateWord + 1
        else:
            MergeWord.append(T2[ch][0])

    # print('重复次数 = ' + str(duplicateWord))
    # 打印合并关键词
    # print(MergeWord)
    return MergeWord


# 得出文档向量
def CalVector(T1, MergeWord):
    TF1 = [0] * len(MergeWord)

    for ch in range(len(T1)):
        TermFrequence = T1[ch][1]
        word = T1[ch][0]
        i = 0
        while i < len(MergeWord):
            if word == MergeWord[i]:
                TF1[i] = TermFrequence
                break
            else:
                i = i + 1
        # print(TF1)
    return TF1


#计算余弦相似度
def CalConDis(v1, v2, lengthVector):
    # 计算出两个向量的乘积
    A1 = 0
    A2 = 0
    B = 0
    i = 0
    while i < lengthVector:
        B = v1[i] * v2[i] + B
        i = i + 1
    # 计算两个向量的模的乘积
    A = 0

    i = 0
    while i < lengthVector:
        A1 = A1 + v1[i] * v1[i]
        i = i + 1
    i = 0
    while i < lengthVector:
        A2 = A2 + v2[i] * v2[i]
        i = i + 1
    A = math.sqrt(A1) * math.sqrt(A2)
    print('Cosine similarity between two articles = ' + format(float(B) / A, ".3f"))





#计算欧几里德距离：
def euclidean(v1,v2):
    same=len(v1)
#计算欧几里德距离,并将其标准化
    e = sum([(v1[i] - v2[i])**2 for i in range(same)])
    print('两篇文章的欧几里得距离 = '+ format(1/(1+e**.5),".3f"))




#计算皮尔逊相关度：
def multipl(a,b):
    sumofab=0.0
    for i in range(len(a)):
        temp=a[i]*b[i]
        sumofab+=temp
    return sumofab

def pearson(x,y):
    n=len(x)
    #求和
    sum1=sum(x)
    sum2=sum(y)
    #求乘积之和
    sumofxy=multipl(x,y)
    #求平方和
    sumofx2 = sum([pow(i,2) for i in x])
    sumofy2 = sum([pow(j,2) for j in y])
    num=sumofxy-(float(sum1)*float(sum2)/n)
    #计算皮尔逊相关系数
    den=sqrt((sumofx2-float(sum1**2)/n)*(sumofy2-float(sum2**2)/n))
    print('两篇文章的皮尔逊相关度 = '+format(num/den,".3f"))

#计算曼哈顿距离：
def manhattan(v1,v2):
    n = len(v1)
    vals = range(n)
    distance = sum(abs(v1[i] - v2[i]) for i in vals)
    print('两篇文章向量的曼哈顿距离 = '+format(distance,".3f"))


#计算jaccard相似系数 （杰卡德相似度计算）
def jaccard_sim(a, b):
    unions = len(set(a).union(set(b)))
    intersections = len(set(a).intersection(set(b)))
    print('两篇文章向量的jaccard相似系数 = '+ format(1. * intersections / unions,".3f"))

#马氏距离计算相似度
def MahalanobisDisSim(x,y):
    npvec1,npvec2=np.array(x),np.array(y)
    npvec=np.array([npvec1, npvec2])
    sub=npvec.T[0]-npvec.T[1]
    inv_sub=np.linalg.inv(np.cov(npvec1, npvec2))
    print('两篇文章向量的马氏距离 = '+ format(math.sqrt(np.dot(inv_sub, sub).dot(sub.T)),".3f"))

# 两篇待比较的文档的路径
sourcefile = '谍影重重.txt'
s2 = '谍影重重2.txt'
# f = csv.reader(open('肖申克的救赎.csv','r'))
# read = list(f)
# for i in read:
#     s2 = str(i[1])+'.txt'
T1 = Count(sourcefile)
print("The word frequency statistics of document 1 are as follows ：")
print(T1)
print()
T2 = Count(s2)
print("文档2的词频统计如下：")
print(T2)
print()
# 合并两篇文档的关键词
mergeword = MergeWord(T1, T2)
# 得出文档向量

v1 = CalVector(T1, mergeword)
print("The vector obtained by vectorization of document 1 is as follows：")
print(v1)
print()
v2 = CalVector(T2, mergeword)
print("The vector obtained by vectorization of document 2 is as follows：")
print(v2)
print()
# 计算余弦距离
CalConDis(v1, v2, len(v1))
#euclidean(v1,v2)
#pearson(v1,v2)
#manhattan(v1,v2)
#jaccard_sim(v1, v2)
#MahalanobisDisSim(v1,v2)
