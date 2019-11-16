import requests
from requests_html import HTML
import concurrent.futures
import time
from decorators import my_time, timer
import itertools
import logging

step = 20
fromc = 421
toc = 720

counter = itertools.count()
t1 = time.time()


#Directory to save the downloaded files
dir = r'D:\One_Piece\\' #include an extra '\'
homepage = requests.get('https://www.mangapanda.com/one-piece')
titles = HTML(html = homepage.text)
titles = titles.find('td')
titles = titles[22:-4:2]


def getchapter(chapter):
    """To change chapter number into desired format for saving"""
    chapter = str(chapter)
    if int(chapter) < 10:
        chapter = '00' + chapter
    elif int(chapter) < 100:
        chapter = '0' + chapter
    return chapter

def getpage(page):
    """To change pages number into desired format for saving"""
    page = str(page)
    if int(page) < 10:
        page = '0' + page
    return page

def download_img(source, name):
    # print(f'Source: {source}')
    # print(f'Name: {name}')
    img = requests.get(source)

    with open(name,'wb') as file:
        file.write(img.content)

    pages = next(counter)

@my_time
def download_chapters(chapter):
    site = 'https://www.mangapanda.com'
    link = '/one-piece/'+str(chapter)
    mangalink = requests.get(site+link)
    html = HTML(html = mangalink.text)
    article = html.find('div#selectpage')
    pages = int(article[0].text.split()[-1])
    for page in range(1,pages+1):
        title = titles[chapter-1].text.split(': ')[-1]
        if title.endswith(':'):
            title = title[:-5]
        # print('Parsing Chapter '+str(chapter)+'. '+title+' Page '+str(page))
        if page != 1:
            mangalink = requests.get(site+link)
            html = HTML(html = mangalink.text)
        image = html.find('div#imgholder',first = True)
        img_src = image.find('img',first = True)
        img_src = img_src.attrs['src']
        # img = requests.get(img_src)
        img_name = dir+getchapter(chapter)+' '+title+' '+getpage(page)+'.jpg'
        # download_img(img_src, img_name)
        with concurrent.futures.ThreadPoolExecutor() as runner:
            runner.submit(download_img, img_src, img_name)

        nextpage = image.find('a', first = True)
        link = nextpage.attrs['href']
    # print(f'---------Chapter {chapter} completed downloading----------')



def download(fromc = 1, toc = 1, step = 10):
    start = end =  fromc
    if toc < fromc:
        toc = fromc
    while end <= toc:
        end += step
        if end > toc:
            end = toc
        chaps = [i for i in range(start, end + 1)]
        print(f'Downloading Chapters {start} to {end}')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(download_chapters, chaps)
            # print('Download complete')
        start += step
        if end == toc:
            break

download(fromc, toc, step = step)
print ('--------------------------------Done--------------------------------------------------------------------')

t2 = time.time()
pages = next(counter) - 1

line = f'Downloaded from Chapter {fromc} to Chapter {toc} at {step} Chapters at a time'
timer.info(line)
line = f'A total {pages-1} pages downloaded in {t2-t1} seconds'
timer.info(line)