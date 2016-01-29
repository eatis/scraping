#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time

# from beautifulsoup4 import beautifulsoup4
from bs4 import BeautifulSoup

BASE_URL = u"http://www.shijou-nippo.metro.tokyo.jp/"

def download_file(url):
    """URL を指定してカレントディレクトリにファイルをダウンロードする
    """
    # print(url)
    if requests.get(url).status_code != 200:
        return ''

    filename = url.split('/')[-1]
    date = url.split('/')[-3]
    for key, value in dict.items():
        # print(key, value, filename)
        if filename.find(key) > -1:
            filename = 'data/' + date + '_' + value + '.csv'

    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return filename

dict = {
    'Kak_K0' : 'all',
    'Kak_K1' : '北足立市場',
    'Kak_K2' : '大田市場',
    'Kak_K3' : '板橋市場',
    'Kak_K4' : '葛西市場',
    'Kak_K5' : '世田谷市場'
}

# http://www.shijou-nippo.metro.tokyo.jp/SN/200401/20040105/Kak/Kak_K0.csv
# http://www.shijou-nippo.metro.tokyo.jp/SN/200401/20040105/Kak/Kak_k0.csv

download_urls = []
for year in range(2008, 2017):
    for month in range(1, 13):
        yearMonth = ''
        yearMonth += 'SN/' + str(year)
        yearMonth += str('{0:02d}'.format(month))
        for day in range(1, 32):
            dayUrl = ''
            dayUrl += yearMonth + '/'
            dayUrl += str(year)
            dayUrl += str('{0:02d}'.format(month))
            dayUrl += str('{0:02d}'.format(day))
            for num in range(0, 6):
                url = ''
                url += dayUrl + '/Kak/Kak_K' + str(num) + '.csv'
                download_urls.append(url)


# ファイルのダウンロード（ひとまず3件に制限）
# 回す時は制限を取って回す
for download_url in download_urls:

    # 一秒スリープ
    # time.sleep(1)

    file_name = download_url.split("/")[-1]

    if BASE_URL in download_url:
        filename = download_file(download_url)
    else:
        filename = download_file(BASE_URL + download_url)

    if filename:
        print('{} is downloaded.'.format(filename))
