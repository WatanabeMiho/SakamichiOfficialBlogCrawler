# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import datetime
import os
import urllib.request
import contextlib
import requests
import time
import math
import random
import selenium
from selenium import webdriver

# year = datetime.date.today().year
# month = datetime.date.today().month
# day = datetime.date.today().day
# todaytime = '%d.%d%02d' % (year, month, day)


def validblogurl(url):
    try:
        urlopen(url)
    except urllib.request.HTTPError:
        return False
    with contextlib.closing(urlopen(url)) as temphandle:
        temphtml = temphandle.read()
        tempsoup = BeautifulSoup(temphtml, 'lxml')

        # if the page is not found then skip
        if 'ページが見つかりません' in (tempsoup.getText()):
            return False
        else:
            return True


# get latest id of post in the website as end
def getlastkeyakiblogid(url):
    indexhandle = urlopen(url)
    mainbloghead = indexhandle.read()
    mainblogsoup = BeautifulSoup(mainbloghead, 'lxml')
    last_blog_url = mainblogsoup.find('div', {'class': 'innerHead'})
    last_url_end = last_blog_url.find('a').attrs['href'].rsplit('/')[-1]
    lastid = last_url_end.split('?')[0]
    return lastid


def getlasthinatablogid(url):
    indexhandle = urlopen(url)
    mainbloghead = indexhandle.read()
    mainblogsoup = BeautifulSoup(mainbloghead, 'lxml')
    last_blog_url = mainblogsoup.find('div', {'class': 'p-blog-top__contents'})
    last_url_end = last_blog_url.find('a').attrs['href'].rsplit('/')[-1]
    lastid = last_url_end.split('?')[0]
    return lastid


def process_keyaki_blog(soup):
    # get blog title as file name
    date = soup.find('div', {'class': 'box-date'}).stripped_strings
    newdate = '.'.join(s for s in date)
    ttl = soup.find('div', {'class': 'box-ttl'}).find('p', {'class': 'name'})
    name = ttl.getText().strip()
    head = soup.find('div', {'class': 'box-ttl'}).find('h3').getText()
    title = '%s %s %d' % (name, newdate, blog_id)
    month = title.rsplit('.', 1)[0]

    # get blog text
    # delete multiple spaces
    # blog = re.split(r'\s{2,}', ' ', blog)
    blog = newdate + '\n' + head + name + '\n'

    blog_string = soup.find('div', {'class': 'box-article'})
    blog_string = str(blog_string).replace('<br/>', '\n')
    blog_string = blog_string.replace('<br>', '\n')
    blog_string = BeautifulSoup(blog_string, 'lxml')
    blog += blog_string.get_text()

    # delete multiple linebreaks
    # blog = re.sub(r'(?<!\n)\n(?!\n)|\n{3,}', '\n', blog)
    # blog = re.sub(r'\n{3,}', '\n\n', blog)

    bottom = soup.find('div', {'class': 'box-bottom'}).getText()
    blog += bottom

    # create new path and save txt
    newpath = r'/Users/Bill/Desktop/LL/keyakiblog/%s/%s/%s' % (name, month, title)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    # else:
    #     continue
    with open(os.path.join(newpath, title + '.txt'), 'wb') as temp_file:
        temp_file.write(blog.encode(encoding='utf-8', errors='strict'))
        temp_file.close()

    # find image urls in blog area from html
    imgs = soup.find('div', {'class': 'box-article'}).findAll('img')
    imglinks = []
    for line in imgs:
        if line is not None:
            try:
                imglinks.append(line.attrs['src'])
            except:
                print(line)

    # search through the urls and save the image into same path as blog
    for img in imglinks:
        if img:
            imgurl = str(img)
            imgname = str(img).split('/')[-1]
            imgpath = os.path.join(newpath, imgname)
            urllib.request.urlretrieve(imgurl, imgpath)

    # find all linked img urls
    img_outside_sources = soup.find('div', {'class': 'box-article'}).findAll('a')
    if img_outside_sources:
        # virtual_browser = webdriver.PhantomJS
        # ('/Users/Bill/PycharmProjects/keyaki/phantomjs-2.1.1-macosx/bin/phantomjs')

        newpath_big = os.path.join(newpath, 'big')
        if not os.path.exists(newpath_big):
            os.makedirs(newpath_big)

        count = 1
        for img_outside in img_outside_sources:
            if img_outside.find('img'):

                img_url1 = img_outside.attrs['href']
                # print(img_url1)
                s = requests.session()
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                                  'AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 '
                                  'Chrome/59.0.3071.115 Safari/603.3.8'
                }
                response = s.get(img_url1, headers=headers)
                with contextlib.closing(urlopen(img_url1)) as temp_img1:
                    contents_awalkers = BeautifulSoup(temp_img1.read(), 'lxml').find('div', {'id': 'contents'})
                    img_url2 = contents_awalkers.find('img').attrs['src']
                    if img_url2[0:4] != 'http':
                        img_url2 = 'http://dcimg.awalker.jp/' + img_url2
                    img2_res = s.get(img_url2, headers=headers)
                # print(response, img2_res)

                deco_img2_name = name + '_' + str(blog_id) + '_' + str(count) + '.jpg'
                with open(os.path.join(newpath_big, deco_img2_name), 'wb') as saving_img:
                    saving_img.write(img2_res.content)
                    saving_img.close()

                img_url5 = str(img_url2).replace('img2', 'img5')
                img5_res = s.get(img_url5, headers=headers)
                # time.sleep(30)

                if img5_res:
                    deco_img5_name = name + '_' + str(blog_id) + '_' + str(count) + '_img5.jpg'

                    with open(os.path.join(newpath_big, deco_img5_name), 'wb') as saving_img:
                        saving_img.write(img5_res.content)
                        saving_img.close()

                    # picSize = os.path.getsize(os.path.join(newpath_big, deco_img5_name))
                    # print(picSize)
                    # if int(picSize) == 0:
                    #     os.remove(os.path.join(newpath_big, deco_img5_name))
                    #     deco_png5_name = name + '_' + str(blog_id) + '_' + str(count) + '_img5.png'
                    #     with open(os.path.join(newpath_big, deco_png5_name), 'wb') as saving_img:
                    #         if not os.path.exists(os.path.join(newpath_big, deco_png5_name)):
                    #             saving_img.write(img5_res.content)
                    #         saving_img.close()
                count = count + 1


def process_hinata_blog(soup):
    # get blog title as file name
    date = soup.find('div', {'class': 'c-blog-article__date'})
    newdate = date.getText().strip()
    ttl = soup.find('div', {'class': 'c-blog-article__name'})
    name = ttl.getText().strip()
    head = soup.find('div', {'class': 'c-blog-article__title'}).getText()
    title = '%s %s %d' % (name, newdate.split(' ')[0], blog_id)
    month = title.rsplit('.', 1)[0]

    # get blog text
    # delete multiple spaces
    # blog = re.split(r'\s{2,}', ' ', blog)
    blog = head + '\n' + newdate + '\n' + name + '\n'

    blog_string = soup.find('div', {'class': 'c-blog-article__text'})
    blog_string = str(blog_string).replace('<br/>', '\n')
    blog_string = blog_string.replace('<br>', '\n')
    blog_string = BeautifulSoup(blog_string, 'lxml')
    blog += blog_string.get_text()

    # delete multiple linebreaks
    # blog = re.sub(r'(?<!\n)\n(?!\n)|\n{3,}', '\n', blog)
    # blog = re.sub(r'\n{3,}', '\n\n', blog)

    # create new path and save txt
    newpath = r'/Users/Bill/Desktop/hinatazaka/hinatablog/%s/%s/%s' % (name, month, title)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    # else:
    #     continue
    with open(os.path.join(newpath, title + '.txt'), 'wb') as temp_file:
        temp_file.write(blog.encode(encoding='utf-8', errors='strict'))
        temp_file.close()

    # find image urls in blog area from html
    imgs = soup.find('div', {'class': 'c-blog-article__text'}).findAll('img')
    imglinks = []
    for line in imgs:
        if line is not None:
            try:
                imglinks.append(line.attrs['src'])
            except:
                print(line)

    # search through the urls and save the image into same path as blog
    for img in imglinks:
        if img:
            imgurl = str(img)
            imgname = str(img).split('/')[-1]
            imgpath = os.path.join(newpath, imgname)
            urllib.request.urlretrieve(imgurl, imgpath)

    # find all linked img urls
    img_outside_sources = soup.find('div', {'class': 'c-blog-article__text'}).findAll('a')
    if img_outside_sources:
        # virtual_browser = webdriver.PhantomJS
        # ('/Users/Bill/PycharmProjects/keyaki/phantomjs-2.1.1-macosx/bin/phantomjs')

        newpath_big = os.path.join(newpath, 'big')
        if not os.path.exists(newpath_big):
            os.makedirs(newpath_big)

        count = 1
        for img_outside in img_outside_sources:
            if img_outside.find('img'):

                img_url1 = img_outside.attrs['href']
                # print(img_url1)
                s = requests.session()
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                                  'AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 '
                                  'Chrome/59.0.3071.115 Safari/603.3.8'
                }
                response = s.get(img_url1, headers=headers)
                with contextlib.closing(urlopen(img_url1)) as temp_img1:
                    contents_awalkers = BeautifulSoup(temp_img1.read(), 'lxml').find('div', {'id': 'contents'})
                    img_url2 = contents_awalkers.find('img').attrs['src']
                    if img_url2[0:4] != 'http':
                        img_url2 = 'http://dcimg.awalker.jp/' + img_url2
                    img2_res = s.get(img_url2, headers=headers)
                # print(response, img2_res)

                deco_img2_name = name + '_' + str(blog_id) + '_' + str(count) + '.jpg'
                with open(os.path.join(newpath_big, deco_img2_name), 'wb') as saving_img:
                    saving_img.write(img2_res.content)
                    saving_img.close()

                img_url5 = str(img_url2).replace('img2', 'img5')
                img5_res = s.get(img_url5, headers=headers)
                # time.sleep(30)

                if img5_res:
                    deco_img5_name = name + '_' + str(blog_id) + '_' + str(count) + '_img5.jpg'

                    with open(os.path.join(newpath_big, deco_img5_name), 'wb') as saving_img:
                        saving_img.write(img5_res.content)
                        saving_img.close()

                    # picSize = os.path.getsize(os.path.join(newpath_big, deco_img5_name))
                    # print(picSize)
                    # if int(picSize) == 0:
                    #     os.remove(os.path.join(newpath_big, deco_img5_name))
                    #     deco_png5_name = name + '_' + str(blog_id) + '_' + str(count) + '_img5.png'
                    #     with open(os.path.join(newpath_big, deco_png5_name), 'wb') as saving_img:
                    #         if not os.path.exists(os.path.join(newpath_big, deco_png5_name)):
                    #             saving_img.write(img5_res.content)
                    #         saving_img.close()
                count = count + 1


baseurl_keyaki = 'http://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000'
baseurl_hinata = 'https://www.hinatazaka46.com/s/official/diary/member?ima=0000'
lastBlogId = max(getlastkeyakiblogid(baseurl_keyaki),getlasthinatablogid(baseurl_hinata))
print(lastBlogId)

# get last id downloaded in the folder as start
filedir = '/Users/Bill/Desktop/LL/keyakiblog'
with open(os.path.join(filedir, 'id.txt'), 'r+') as idtxt:
    blog_id = int(idtxt.read())
    print(blog_id)
    idtxt.close()

# all_subdirs = []
# for d in os.listdir(dir):
#     if os.path.isdir(os.path.join(dir, d)):
#         all_subdirs.append((dir + '/' + d))
# latest_subdir = max(all_subdirs, key=os.path.getmtime)
# id = int(latest_subdir.split()[-1])


keyaki_blog_url = 'http://www.keyakizaka46.com/s/k46o/diary/detail/%d?ima=0000&cd=member'
hinata_blog_url = 'https://www.hinatazaka46.com/s/official/diary/detail/%d?ima=0000&cd=member'

while True:
    blog_id = blog_id + 1
    # base url
    print(blog_id)
    keyaki_temp_url = keyaki_blog_url % blog_id
    hinata_temp_url = hinata_blog_url % blog_id

    # test it is keyaki or hinata blog
    # if the page is not found then skip
    if validblogurl(keyaki_temp_url):
        blog_url = keyaki_temp_url
        blog_pointer = 'keyaki'
    elif validblogurl(hinata_temp_url):
        blog_url = hinata_temp_url
        blog_pointer = 'hinata'
    else:
        if blog_id > int(lastBlogId):
            blog_id = blog_id - 1
            break
        continue

    with contextlib.closing(urlopen(blog_url)) as handle:
        html = handle.read()
        blog_soup = BeautifulSoup(html, 'lxml')

        if blog_pointer == 'keyaki':
            process_keyaki_blog(blog_soup)
        if blog_pointer == 'hinata':
            process_hinata_blog(blog_soup)

    if blog_id >= int(lastBlogId):
        break

with open(os.path.join(filedir, 'id.txt'), 'wb') as idtxt:
    idtxt.write(str(blog_id).encode(encoding='utf-8', errors='strict'))
    idtxt.close()
