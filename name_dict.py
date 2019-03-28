import re
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import datetime
import os
import urllib.request

names_list = ('石森虹花','今泉佑唯','上村莉菜','尾関梨香','織田奈那','小池美波','小林由依','齋藤冬優花',
             '佐藤詩織','志田愛佳','菅井友香','鈴本美愉','長沢菜々香','土生瑞穂','原田葵','平手友梨奈',
             '守屋茜','米谷奈々未','渡辺梨加','渡邉理佐','井口眞緒','潮紗理菜','柿崎芽実','影山優佳',
             '加藤史帆','齊藤京子','佐々木久美','佐々木美玲','高瀬愛奈','高本彩花','長濱ねる','東村芽依')
id_list = ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','17',
           '18','19','20','21','23','24','25','26','27','28','29','30','31','32','22','33')
name_dict = dict()
for i in range(1,32):
    name_dict[names_list[i]] = id_list[i]
for item in name_dict:
    print(item, name_dict[item])