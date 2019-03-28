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
box = hsoup.find('div', {'class':'sorted sort-birth'})
officialPhotos = box.findAll('a')
dir = '/Users/Bill/Desktop/LL/欅坂公式照/8th-1'
print(dir)
input()
if not os.path.exists(dir):
    os.makedirs(dir)

with open(os.path.join(dir, '8thPhoto.txt'), 'w') as photolinktxt:
    for photo in officialPhotos:
        photolink = photo.find('img').attrs['src']
        photolink = str(photolink).replace('/400_320_102400','')
        name = name = photo.find('p',{'class':'name'}).get_text().strip()
        name = name + '_7' + photolink.split('/')[-1]
        imgpath = os.path.join(dir, name)
        urllib.request.urlretrieve(photolink, imgpath)
        photolinktxt.write(photolink + '\n')
photolinktxt.close()
