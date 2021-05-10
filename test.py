#爬取电影基本信息
import requests
from lxml import etree
import pandas as pd
import os


MOVIES = []
IMGURLS = []

def get_html(url):

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    try:
        html = requests.get(url,headers = headers)
        html.encoding = html.apparent_encoding
        if html.status_code == 200:
            print('Get the source code successfully')
    except Exception as e:
        print('Failed to get source code:%s' % e)
    return html.text

def parse_html(html):
    movies = []
    imgurls = []
    html = etree.HTML(html)
    lis = html.xpath("//ol[@class = 'grid_view']/li")
    for li in lis:
        name = li.xpath(".//a/span[@class='title'][1]/text()")[0]
        director_actor = "".join(li.xpath(".//div[@class='bd']/p/text()[1]")[0].replace(' ','').replace('\n','').replace('/','').split())
        info = "".join(li.xpath(".//div[@class='bd']/p/text()[2]")[0].replace(' ','').replace('\n','').split())
        rating_score = li.xpath(".//span[@class='rating_num']/text()")[0]
        rating_num = li.xpath(".//div[@class='star']/span[4]/text()")[0]
        introduce = li.xpath(".//p[@class='quote']/span/text()")
        imgurl = li.xpath(".//img/@src")[0]
        if introduce:
            movie = {'name': name, 'director_actor': director_actor, 'info': info, 'rating_score': rating_score,
                     'rating_num': rating_num, 'introduce': introduce[0],'imgurl':imgurl}
        else:
            movie = {'name': name, 'director_actor': director_actor, 'info': info, 'rating_score': rating_score,
                     'rating_num': rating_num, 'introduce': None}
        imgurl = li.xpath(".//img/@src")[0]
        movies.append(movie)
        imgurls.append(imgurl)
    return movies,imgurls

def download_img(url,movie):

    if 'movieposter' in os.listdir(r'E:\360MoveData\Users\dell\Desktop\HomeWork\year4\BS'):
        pass
    else:
        os.mkdir('movieposter')
    os.chdir(r'E:\360MoveData\Users\dell\Desktop\HomeWork\year4\BS\movieposter')

    img = requests.get(url).content

    with open(movie['name'] + '.jpg','wb') as f:
        print('正在下载 ： %s' % url)
        f.write(img)



if __name__ == '__main__':

    for i in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='

        html = get_html(url)
        movies = parse_html(html)[0]
        imgurls = parse_html(html)[1]

        MOVIES.extend(movies)
        IMGURLS.extend(imgurls)

    # for i in range(250):
    #     download_img(IMGURLS[i],MOVIES[i])

    os.chdir(r'E:\360MoveData\Users\dell\Desktop\HomeWork\year4\BS')
    moviedata = pd.DataFrame(MOVIES)
    moviedata.to_csv('movie1.csv')
    print('电影信息成功保存到本地')