# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import datetime
import os
import urllib.request
import contextlib
import requests

photosUrlList = ['http://cdn.keyakizaka46.com/images/14/6b6/65108610fbb0f11129d26dfd32004/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/69a/3e5acafa1d4bdf3aabcbcb0b851fa/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/1fc/0a2281d45f3eb487220f34533742d/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/8ca/bc27b28b651bee6b28a8d108f0f73/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/c56/42e41e8a66d4dd9a6e8af8915c39f/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/579/790ed744e913f12a755cdcae3e9e5/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/884/15381ecd65c1a4a6d69b7768a1c1e/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/d8f/24f212838c8eeae711d842152b2c3/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/676/37f3c536e757e377e400cfc8bc93b/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/e37/11187288975309e5f2c6e4f4e6613/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/3fe/e790ddb60351823417e45d6ad04f9/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/883/d080fc6f4ba010274ea827a7d1098/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/085/56bf87f6c750d8037ff02cd594e7b/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/d35/97146cd5c14f1151afe6a52048d3b/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/fef/2a61525b17aa62550077bdbee8c2a/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/3ce/7ccbb5fc836c83649b2e40a8d02f3/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/a9c/db53d72b36429690be6ae3ba093b3/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/d74/3c0447467cb9a6d7307c1f663c670/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/bd8/c74a9a2b4d47f68fff2c8d3025bc8/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/5c6/d639dab36cfadbc7364daf4fcc895/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/370/4c6bbb5e11d81058937e5a0a542e0/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/2d6/a5cca412d49b6edcbee5650af95a5/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/4bb/2f8dd03b5d24fca95458c72a9390c/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/974/b3f2389572c673062bf357dc3399a/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/280/b837c5a7f75ba7cc155c39d033521/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/d1e/934cdfcb661545f099b0477a891f9/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/464/bce2f2123b0e0825bfbd67fe9e54f/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/16c/a9c082cad9555b7ae58ce36c005a7/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/9dc/764567f165ef5672c212b6ef405cd/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/a14/060b99e1ecc13d7c2ca0da314fe65/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/440/58db47442af93e4ba8a7f7facf33c/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/6e5/2d9da70d5b34d079dc693e8f40f5a/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/570/f8869eea7f9ebdd55d1930e3fe661/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/586/664d51cdb8d410a550692f2ec1050/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/082/31dfdc8bab951076fcaf102c535df/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/204/af8f5590b07712f37e3f6c9f40d10/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/f9f/2126cc9ac31f3610f4ba776357b34/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/50c/7a468466df80cde6cd42f4f6e9088/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/c15/6ca2f9934f2c728ec021ccb2e5b03/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/54f/db819afb7d07b872b919fd3c748ba/400_640_102400.jpg',
                 'http://cdn.keyakizaka46.com/images/14/675/fa86fe86eec60963dcb7dd5d46db1/400_640_102400.jpg']

for img in photosUrlList:
    if img:
        imgUrl = str(img).replace('/400_640_102400', '')
        imgName = str(imgUrl).split('/')[-1]
        imgPath = os.path.join('/Users/Bill/Desktop/LL/欅坂公式照/真っ白/', imgName)
        urllib.request.urlretrieve(imgUrl, imgPath)
