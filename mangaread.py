import requests
from requests_html import HTML

#downloads all chapters from fromc to toc
fromc = 1
toc = 1
#downloads to directory
dir = r'D:\One_Piece\\' #include an extra '\'


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

homepage = requests.get('https://www.mangapanda.com/one-piece')
titles = HTML(html = homepage.text)
titles = titles.find('td')
titles = titles[22:-4:2]

site = 'https://www.mangapanda.com'

for chapter in range(fromc,toc+1):


    link = '/one-piece/'+str(chapter)


    mangalink = requests.get(site+link)

    html = HTML(html = mangalink.text)
    article = html.find('div#selectpage')
    pages = int(article[0].text.split()[-1])


    for page in range(1,pages+1):
        print('Parsing Chapter '+str(chapter)+'. '+titles[chapter-1].text.split(': ')[-1]+' Page '+str(page))
        if page != 1:
            mangalink = requests.get(site+link)
            html = HTML(html = mangalink.text)
        image = html.find('div#imgholder',first = True)
        img_src = image.find('img',first = True)
        img_src = img_src.attrs['src']

        img = requests.get(img_src)

        with open(dir+getchapter(chapter)+' '+titles[chapter-1].text.split(' : ')[-1]+' '+getpage(page)+'.jpg','wb') as file:
            file.write(img.content)

        nextpage = image.find('a', first = True)
        link = nextpage.attrs['href']

print ('Done')


