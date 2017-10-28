#coding=utf-8
import urllib2
import os
from lxml import etree

def getPageLink(url,begin,end):
    """
    获取小组主页全部帖子链接
    :param url:
    :return:
    """
    #构建所有URL
    urlList = []
    #构建所有需要获取的链接
    for page in range(begin,end+1):
        pn = (page - 1) * 25
        urlList.append(str(url)+str(pn))
    #构建head
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    #存放所有帖子链接
    linkList = []
    for i in urlList:
        Request =  urllib2.Request(i,headers=headers)
        html = urllib2.urlopen(Request).read()
        content=etree.HTML(html)
        #用xpath获取链接
        tempList=content.xpath('//td[@class="title"]/a/@href')
        for t in tempList:
            linkList.append(t)
    getImgLink(linkList)
def getImgLink(url):
    """
    获取帖子里所有图片的链接
    :param url:
    :return:
    """
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.douban.com/group/haixiuzu/discussion?start=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    imgUrl = []
    for t in url:
        request = urllib2.Request(t,headers=headers)
        html = urllib2.urlopen(request).read()
        content = etree.HTML(html)
        #用xpath获取所有图片链接
        tempList = content.xpath('//div[@class="topic-content"]/div[@class="topic-figure cc"]/img/@src')
        for t in tempList:
            imgUrl.append(t)
    savaImg(imgUrl)


def savaImg(imgList):
    """
    保存图片到本地
    :param imgList:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    #判断目录是否存在
    isExists = os.path.exists('img')
    #如果不存在创建
    if not isExists:
        os.makedirs('img')
    for t in imgList:
        request =  urllib2.Request(t,headers=headers)
        img = urllib2.urlopen(request).read()
        fileName = t[-10:]
        #写图片到指定目录
        with open('img\\'+fileName,"wb") as writ:
            writ.write(img)


#判断是否是模块运行
if __name__=="__main__":
    url = raw_input('请输入小组字符串代码如:haixiuzu')
    beginPage = int(raw_input('请输入起始页码'))
    endPage= int(raw_input('请输入结束页码'))
    #构建url
    url = 'https://www.douban.com/group/'+url+'/discussion?start='
    #获取所有url
    getPageLink(url,beginPage,endPage)
