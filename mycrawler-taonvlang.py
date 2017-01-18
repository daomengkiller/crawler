import re
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import urllib.request

browserPath = r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe'
homePage = r'https://mm.taobao.com/?spm=719.7763510.1998606017.1.NOC5nB'
outputDir = 'D:\\myphoto'
parser = 'html5lib'


# driver = webdriver.PhantomJS(executable_path=browserPath)
# driver.get(homePage)
# print(driver.find_element_by_id('J_tab').text.split('\n'))
# bsObj = BeautifulSoup(driver.page_source, parser)
# girlsUrl = bsObj.find_all("a", {"href": re.compile("\/\/.*\.htm\?(pic_id=)\d*")})
# imagesUrl = re.findall('https:\/\/img.alicdn.com\/imgextra\/i3\/.*\.jpg_360x360xz\.jpg')


def main():
    driver = webdriver.PhantomJS(executable_path=browserPath)#加载虚拟浏览器
    driver.get(homePage)#打开网页
    bsObj = BeautifulSoup(driver.page_source, parser)#将网页源码已html5的规则解析，返回所有标签
    print("[*]OK GET Page")
    girlsList = driver.find_element_by_id("J_tab").text.split('\n')#寻找元素ID,确定需要的信息在哪个大类里
    imagesUrl = re.findall('https:\/\/img.alicdn.com\/imgextra\/i[0-9]\/.*\.*g_360x360xz\.jpg',driver.page_source)#获取图片地址
    girlsUrl = bsObj.find_all("a", {"href": re.compile("\/\/.*\.htm\?(pic_id=)\d*")})#获取妹子主页地址
    girlsNL = girlsList[0::3]#以每3个进行切分提取
    #girlsHW = girlsList[1::3]#已第一个为序列每3个切分提取
    girlsHURL = [('http:' + i['href']) for i in girlsUrl]#保存妹子主页的地址列表
    girlsPhotoURL = [('https:' + i) for i in imagesUrl]#保存妹子的图片，第一张
    girlsInfo = zip( girlsHURL, girlsPhotoURL)#将妹子的所有信息组成可迭代的tuple组合，个人感觉是tuple的list
    for girlHURL, girlCover in girlsInfo:#循环抽取妹子的信息，组成文件夹
        print("[*]Girl:", 1, 2)#打印姓名地址，身高体重
        mkdir(outputDir)#建立以妹子为名字的文件夹
        print("   [*]saving...")
        data = urlopen(girlCover).read()#读取妹子主页的消息
        with open(outputDir  + '/cover.jpg', 'wb')as f:#写入数据
            f.write(data)
        print("  [+]Loading Cover...")
        getImgs(girlHURL, outputDir )#下载图片
    driver.close()


def mkdir(path):#建立文件夹
    isExists = os.path.exists(path)
    if not isExists:
        print("[*]新建了文件夹", path)
        os.makedirs(path)
    else:
        print(' [+]文件夹', path, '已创建')


def getImgs(url, path):#
    driver = webdriver.PhantomJS(executable_path=browserPath)
    driver.get(url)
    print("  [*]Opening...")
    bsObj = BeautifulSoup(driver.page_source, parser)
    imgs = bsObj.find_all ("imgs", {"src": re.compile(".*\.jpg")})
    for i, img in enumerate(imgs[1:]):
        try:
            html = urlopen('https:' + img['src'])
            data = html.read()
            fileName = "{}/{}.jpg".format(path, i + 1)
            print("  [+]Loading...", fileName)
            with open(fileName, 'wb')as f:
                f.write(data)
        except Exception:
            print("  [!]Address Error!")
    driver.close()
def saveHtml(filename,filecontent):
    with open (filename.replace('/','_')+'.html','wb')as f:
        f.write(filecontent)
        return f

if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    main()
