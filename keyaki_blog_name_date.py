import re
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import datetime
from datetime import timedelta
import os
import urllib.request
import contextlib
import urllib.parse

names_user = []
today = datetime.date.today()

with open('开始和结束日期.txt', 'r') as datetxt:
    start_date = datetxt.readline().strip()
    end_date = datetxt.readline().strip()
    datetxt.close()

with open('last_update.txt', 'r') as last_date_txt:
    last_date = last_date_txt.readline().strip()
    last_date_txt.close()

with open('成员列表.txt', 'r') as member_txt:
    while True:
        line = member_txt.readline()
        if line:
            names_user.append(line)
        else:
            break
    member_txt.close()

parent_path = os.getcwd()

full_names_list = ('石森虹花','今泉佑唯','上村莉菜','尾関梨香','織田奈那','小池美波','小林由依','齋藤冬優花',
             '佐藤詩織','志田愛佳','菅井友香','鈴本美愉','長沢菜々香','土生瑞穂','原田葵','平手友梨奈',
             '守屋茜','米谷奈々未','渡辺梨加','渡邉理佐','井口眞緒','潮紗理菜','柿崎芽実','影山優佳',
             '加藤史帆','齊藤京子','佐々木久美','佐々木美玲','高瀬愛奈','高本彩花','長濱ねる','東村芽依')

id_list = ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','17',
           '18','19','20','21','23','24','25','26','27','28','29','30','31','32','22','33')

name_dict = dict()

for i in range(1,32):
    name_dict[full_names_list[i]] = id_list[i]

fundamental_url = 'http://www.keyakizaka46.com'

if start_date:
    start = datetime.datetime.strptime(start_date,'%Y%m%d')
elif last_date:
    start = datetime.datetime.strptime(last_date,'%Y%m%d')
else:
    start = today

if end_date:
    end = datetime.datetime.strptime(end_date,'%Y%m%d')
else:
    end = today

daycount = (end - start).days + 1
blog_url_list = []

for name in names_user:
    temp_id = name_dict[name]
    for count in range(0, daycount):
        temp_day = start + timedelta(count)
        daily_url_user = 'http://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000&ct=%s&dy=%s' \
                         %(temp_id, datetime.date.strftime(temp_day, '%Y%m%d'))
        try:
            with contextlib.closing(urlopen(daily_url_user)) as handle:
                html = handle.read()
                soup = BeautifulSoup(html, 'lxml')
                text = soup.find('div',{'class':'box-main'}).get_text()
                if '記事がありません' in text:
                    continue
                blog_ttl = soup.findAll('div',{'class':'box-ttl'})
                for item in blog_ttl:
                    blog_url_list.append(item.find('a').attrs['href'])
            handle.close()
        except urllib.request.HTTPError:
            continue

for blog_url in blog_url_list:
    full_blog_url = urllib.parse.urljoin(fundamental_url, blog_url)
    try:
        with contextlib.closing(urlopen(full_blog_url)) as handle:
            html = handle.read()
            soup = BeautifulSoup(html, 'lxml')

            # if the page is not found then skip
            if 'ページが見つかりませんでした' in (soup.getText()):
                continue
            # get blog title as file name
            date = soup.find('div',{'class':'box-date'}).stripped_strings
            newdate = '.'.join(s for s in date)
            ttl = soup.find('div',{'class':'box-ttl'}).find('p',{'class':'name'})
            name = ttl.getText().strip()
            head = soup.find('div',{'class':'box-ttl'}).find('h3').getText()
            title = '%s %s %d' % (name, newdate, id)
            month = title.rsplit('.', 1)[0]

            # get blog text
            # delete multiple spaces
            # blog = re.split(r'\s{2,}', ' ', blog)
            blog = newdate + '\n' + head + name + '\n'

            blog_string = soup.find('div', {'class': 'box-article'})
            blog_string = str(blog_string).replace('<br/>', '\n')
            blog_string = str(blog_string).replace('<br>', '\n')
            blog_string = BeautifulSoup(blog_string, 'lxml')
            blog += blog_string.get_text()

            # blog_string = soup.find('div', {'class': 'box-article'}).strings
            # for line in blog_string:
            #     if '\n' in line:
            #         blog += line
            #     else:
            #         blog += (line + '\n')

            # delete multiple linebreaks
            # blog = re.sub(r'(?<!\n)\n(?!\n)|\n{3,}', '\n', blog)

            blog = re.sub(r'\n{3,}', '\n\n', blog)

            bottom = soup.find('div', {'class': 'box-bottom'}).getText()
            blog += bottom

            # create new path and save txt
            newpath = os.path.join(parent_path, name, month, title)
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
    except urllib.error.HTTPError:
        continue

with open('last_update.txt', 'wb') as last_date_txt:
    last_date_txt.write(datetime.date.strftime(end,'%Y%m%d').encode(encoding='utf-8', errors='strict'))
    last_date_txt.close()