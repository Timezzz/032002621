import os
import asyncio
from pyppeteer import launcher
from pyppeteer import launch
from bs4 import BeautifulSoup


async def pyppteer_fetchUrl(url):
    browser = await launch({'headless': False,'dumpio':True, 'autoClose':True})
    page = await browser.newPage()

    await page.goto(url)
    await asyncio.wait([page.waitForNavigation()])
    str = await page.content()
    await browser.close()
    return str

def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))
#使用pyppeteer来爬取页面内容

def getPageUrl():
    for page in range(1,42):
        if page == 1:
            yield 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
        else:
            url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_'+ str(page) +'.shtml'
            yield url
#网页是利用url来进行翻页的，此函数用来构造不同页面的url
def getTitleUrl(html):

    bsobj = BeautifulSoup(html,'html.parser')
    titleList = bsobj.find('div', attrs={"class":"list"}).ul.find_all("li")
    for item in titleList:
        link = "http://www.nhc.gov.cn" + item.a["href"]
        title = item.a["title"]
        date = item.span.text
        yield title, link, date
#此函数用来得到每个疫情通报的标题，链接和日期
def getContent(html):

    bsobj = BeautifulSoup(html,'html.parser')

    try:
        cnt = bsobj.find('div', attrs={"id":"xw_box"}).find_all("p")
    except AttributeError:
        return "爬取失败！"
    s = ""
    if cnt:
        for item in cnt:
            s += item.text
        return s

    return "爬取失败！"
#疫情通报详细文本信息放着网页的xw_box下，此函数用来爬取疫情通报的文本信息
def saveFile(path, filename, content):

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + filename + ".txt", 'w', encoding='utf-8') as f:
        f.write(content)
#此函数用来将疫情通报的信息以.txt文件形式保存
if "__main__" == __name__:
    for url in getPageUrl():
        s =fetchUrl(url)
        for title,link,date in getTitleUrl(s):
            print(title,link)
            #如果日期在1月21日之前，则直接退出
            mon = int(date.split("-")[1])
            day = int(date.split("-")[2])
            if mon <= 1 and day < 21:
                break;

            html =fetchUrl(link)
            content = getContent(html)
            print(content)
            saveFile("D:/Python/mydatas/", title, content)
            print("-----"*20)
