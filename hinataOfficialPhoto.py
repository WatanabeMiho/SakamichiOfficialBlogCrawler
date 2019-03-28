from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import os
import datetime
import urllib.request
import contextlib

baseurl = 'https://www.hinatazaka46.com/s/official/search/artist?ima=0000'
index = urlopen(baseurl)
head = index.read()
hsoup = BeautifulSoup(head, 'lxml')
box = hsoup.find('div', {'class':'l-container'})
officialPhotos = box.findAll('a')
dir = '/Users/Bill/Desktop/Hinatazaka/日向坂公式照/1th'
print(dir)
input()
if not os.path.exists(dir):
    os.makedirs(dir)

with open(os.path.join(dir, '1thPhoto.txt'), 'w') as photolinktxt:
    for photo in officialPhotos:
        photolink = photo.find('img')
        if photolink is not None:
            photolink = str(photolink.attrs['src']).replace('/400_320_102400','')
            name = photo.find('div', {'class': 'c-member__name'}).get_text().strip()
            name = name + '_7' + photolink.split('/')[-1]
            imgpath = os.path.join(dir, name)
            urllib.request.urlretrieve(photolink, imgpath)
            photolinktxt.write(photolink + '\n')
photolinktxt.close()
