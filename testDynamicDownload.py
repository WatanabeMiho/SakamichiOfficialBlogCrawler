# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import time
import os
import urllib.request
import contextlib
import requests
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tkinter import Tk

blog_id = 11141
# base url
blog_url = 'http://www.keyakizaka46.com/s/k46o/diary/detail/%d?ima=0000&cd=member' % blog_id
# print(blog_url)
with contextlib.closing(urlopen(blog_url)) as handle:
    html = handle.read()
    soup = BeautifulSoup(html, 'lxml')

    # if the page is not found then skip

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
            imglinks.append(line.attrs['src'])

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
        os.makedirs(newpath_big)

        count = 1
        for img_outside in img_outside_sources:
            if img_outside.find('img'):

                img_url1 = img_outside.attrs['href']
                # print(img_url1)
                s = requests.session()
                headers = {
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                                 'AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 '
                                 'Chrome/59.0.3071.115 Safari/603.3.8'
                }
                response = s.get(img_url1, headers=headers)
                with contextlib.closing(urlopen(img_url1)) as temp_img1:
                    contents_awalkers = BeautifulSoup(temp_img1.read(), 'lxml').find('div', {'id': 'contents'})
                    img_url2 = contents_awalkers.find('img').attrs['src']
                img2_res = s.get(img_url2, headers=headers)
                # print(response, img_res)

                deco_img2_name = name + '_' + str(blog_id) + '_' + str(count) + '.jpg'
                with open(os.path.join(newpath_big, deco_img2_name), 'wb') as saving_img:
                    saving_img.write(img2_res.content)
                    saving_img.close()

                img_url5 = str(img_url2).replace('img2','img5')
                img5_res = s.get(img_url5, headers=headers)
                if img5_res:
                    deco_img5_name = name + '_' + str(blog_id) + '_' + str(count) + '_img5.jpg'

                    with open(os.path.join(newpath_big, deco_img5_name), 'wb') as saving_img:
                        saving_img.write(img5_res.content)
                        saving_img.close()
                count = count + 1
                # virtual_browser = webdriver.Chrome('/usr/local/bin/chromedriver')
                # virtual_browser.get(img_url1)
                # deco_img = virtual_browser.find_element_by_xpath('//div[@id="contents"]/img')
                # print(deco_img)
                # time.sleep(5)
                # deco_action = ActionChains(virtual_browser).move_to_element(deco_img)
                # deco_action.context_click(deco_img)
                # deco_action.send_keys(Keys.ARROW_DOWN)
                # deco_action.send_keys(Keys.ARROW_DOWN)
                # deco_action.perform()
                # img_memory = read_memory.clipboard_get()
                #
                #     virtual_browser.get(img_url2)
                # virtual_browser.get_screenshot_as_file(os.path.join(newpath, deco_img_name))

                # virtual_browser.close()

