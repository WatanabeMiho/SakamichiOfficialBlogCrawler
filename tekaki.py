from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import os
import datetime
import urllib.request
import contextlib

baseurl = 'http://www.keyakizaka46.com/s/k46o/search/artist?ima=0000'
index = urlopen(baseurl)
head = index.read()
hsoup = BeautifulSoup(head, 'lxml')
box = hsoup.find('div', {'class':'sorted sort-constellation'})
members = box.findAll('a')
memberpages = [line.attrs['href'] for line in members]

date = hsoup.find('li',{'class':'news'}).find('a').attrs['href'].rsplit('=', 1)[1]
dir = '/Users/Bill/Desktop/LL/欅坂手書き/%s/' % date
print(dir)
input("Continue:")
if not os.path.exists(dir):
    os.makedirs(dir)

with open(os.path.join(dir, '%s_tekaki.txt' % date), 'w') as photolinktxt:
    for line in memberpages:
        link = 'http://www.keyakizaka46.com' + line

        with contextlib.closing(urlopen(link)) as handle:
            html = handle.read()
            soup = BeautifulSoup(html, 'lxml')

            name = soup.find('p',{'class':'name'}).get_text().strip()
            # name = name + '_手書き_' + date + '.jpg'

            imgsrc = soup.find('div',{'class':'box-msg'}).find('img')
            if imgsrc is None:
                print(link)
                continue
            tekaki = imgsrc.attrs['src']
            name = name + '_手書き_' + date + str(tekaki).split('/')[-1]
            imgpath = os.path.join(dir, name)
            urllib.request.urlretrieve(tekaki, imgpath)
            photolinktxt.write(str(tekaki) + '\n')
photolinktxt.close()
