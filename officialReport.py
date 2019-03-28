from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import os
import datetime
import urllib.request
import contextlib

baseurl = 'http://www.keyakizaka46.com/mob/news/diarShw.php?site=k46o&ima=0000&cd=report'
index = urlopen(baseurl)
head = index.read()
hsoup = BeautifulSoup(head, 'lxml')
box = hsoup.findAll('div', {'class':'box-sub'})
reportpages = [line.find('a').attrs['href'] for line in box]

# date = hsoup.find('li',{'class':'news'}).find('a').attrs['href'].rsplit('=', 1)[1]
dir = '/Users/Bill/Desktop/LL/keyaki_report/'

# for line in reportpages:
line = reportpages[0]
link = 'http://www.keyakizaka46.com' + line
id = link.split('/')[-1][0:4]
print(id)
with contextlib.closing(urlopen(link)) as handle:
    html = handle.read()
    soup = BeautifulSoup(html, 'lxml')

    repo_title = soup.find('div', {'class': 'header-box'})
    ttl = repo_title.find('p', {'class': 'ttl'}).get_text().strip()
    ttl = str(ttl).replace('/', '')
    date = repo_title.find('time').get_text()

    repo_text = ttl + '\n' + date

    repo_main = soup.find('div', {'class': 'box-content'})
    text_main = str(repo_main.find('p')).replace('<br/>', '\n')
    rebuild_text = BeautifulSoup(text_main, 'lxml')
    text_link = rebuild_text.findAll('a')
    repo_text += rebuild_text.get_text()
    if text_link:
        for link in text_link:
            if link:
                repo_text += link.attrs['href']

    temp_path = dir + ttl + ' ' + date + ' ' + id
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    # else:
        # continue

    with open(os.path.join(temp_path, ttl + '.txt'), 'wb') as temp_file:
        temp_file.write(repo_text.encode(encoding='utf-8', errors='strict'))
        temp_file.close()

    imgs = repo_main.findAll('img')
    imglinks = []
    for line in imgs:
        if line is not None:
            imglinks.append(line.attrs['src'])

    for img in imglinks:
        if img:
            url = '' + str(img)
            imgname = str(img).rsplit('/', 1)[1]
            imgpath = os.path.join(temp_path, imgname)
            if ' ' in url:
                url = url.replace(' ', '%20')
            urllib.request.urlretrieve(url, imgpath)
