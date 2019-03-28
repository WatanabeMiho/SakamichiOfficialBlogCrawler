import os
import sys
from pathlib import Path
import pathlib
import csv

dir = '/Users/Bill/Desktop/LL/keyakiblog'
blog_count = 0
blog_text = ''
img_count = 0
output = []
for name in os.listdir(dir):
    if os.path.isdir(os.path.join(dir, name)):
        for path, subdirs, files in os.walk(os.path.join(dir, name)):
            for file in files:
                if file.endswith('.txt'):
                    blog_count += 1
                    with open(os.path.join(path, file), 'r') as temp_file:
                        blog_text += temp_file.read()
                if file.endswith('.jpg') or file.endswith('.png'):
                    img_count += 1
        if blog_count == 0:
            continue
        blog_text.replace(' ', '')
        blog_text.replace('\n', '')
        output.append([name, blog_count, len(blog_text), round(len(blog_text) / blog_count,2),
                       img_count, round(img_count / blog_count,2)])
        blog_count = 0
        blog_text = ''
        img_count = 0

with open(os.path.join(dir, 'keyaki_blog_stat_20180220.txt'), 'w+') as stat_file:
    writer = csv.writer(stat_file)
    writer.writerow(['Name', 'blog数', 'blog总字数', '平均每篇字数', '图片数', '平均每篇图片数'])
    for line in output:
        writer.writerow(line)
stat_file.close()