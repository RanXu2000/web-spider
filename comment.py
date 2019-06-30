# -*-coding:utf-8-*-
import urllib.request

from bs4 import BeautifulSoup

#爬取复联四评论
def getHtml(url):
    """获取url页面"""
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    req = urllib.request.Request(url,headers=headers)
    req = urllib.request.urlopen(req)
    content = req.read().decode('utf-8')

    return content


def getComment(url):
    """解析HTML页面"""
    html = getHtml(url)
    soupComment = BeautifulSoup(html, 'html.parser')

    comments = soupComment.findAll('span', 'short')
    onePageComments = []
    for comment in comments:
        # print(comment.getText()+'\n')
        onePageComments.append(comment.getText()+'\n')

    return onePageComments


if __name__ == '__main__':
    f = open('复仇者联盟4：终局之战 短评page10.txt', 'w', encoding='utf-8')
    for page in range(10):  # 豆瓣爬取多页评论需要验证。
        url = 'https://movie.douban.com/subject/26100958/comments?start=' + str(20*page) + '&limit=20&sort=new_score&status=P'
        print('第%s页的评论:' % (page+1))
        print(url + '\n')

        for i in getComment(url):
            f.write(i)
            print(i)
        print('\n')



#词云可视化评论
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from imageio import imread
import jieba

text = open("复仇者联盟4：终局之战 短评page10.txt","rb").read()
#结巴分词
wordlist = jieba.cut(text,cut_all=True)
wl = " ".join(wordlist)
#print(wl)#输出分词之后的txt


#把分词后的txt写入文本文件
#fenciTxt  = open("fenciHou.txt","w+")
#fenciTxt.writelines(wl)
#fenciTxt.close()


#设置词云
wc = WordCloud(background_color = "white",
               #设置背景颜色
               mask = imread('avengers.png'),
               #设置背景图片
               max_words = 2000,
               #设置最大显示的字数
               stopwords = ["的", "这种", "这样", "还是", "就是", "这个","还有","然而"],
               #设置停用词
               font_path = "C:\Windows\WinSxS\simkai.ttf",
               #设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
               max_font_size = 100,
               #设置字体最大值
               random_state = 30,
               #设置有多少种随机生成状态，即有多少种配色方案
    )
myword = wc.generate(wl)
#生成词云
wc.to_file('result.jpg')

#展示词云图
plt.imshow(myword)
plt.axis("off")
plt.show()


#情感分析
import numpy as np
from snownlp import SnowNLP
import matplotlib.pyplot as plt



# SnowNLP是python中用来处理文本内容的，可以用来分词、标注、文本情感分析等，情感分析是简单的将文本分为两类，积极和消极，返回值为情绪的概率，越接近1为积极，接近0为消极

f = open('复仇者联盟4：终局之战 短评page10.txt', 'r', encoding='UTF-8')
list = f.readlines()
sentimentslist = []
for i in list:
    s = SnowNLP(i)
    # print s.sentiments
    sentimentslist.append(s.sentiments)
plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01), facecolor='b')
plt.xlabel('Chance')
plt.ylabel("Quantity")
plt.title('Analysis of Avengers 4')
plt.show()

print("程序到此结束，后续有待改善")