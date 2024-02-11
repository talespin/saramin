#!/usr/bin/python
"""
:filename: 3.saramin_crawler_one.py
:author: 최종환
:last update: 2024.01.11
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    saramin 옵션으로 지정한 json 파일을 읽어서 해당파일의 목록일 이용하여 컨텐츠를 크롤한다.
 
"""
import os
import sys
import socket
import urllib3
import logging
import argparse
import pandas as pd
import requests as req
from random import random
from time import sleep
from bs4 import BeautifulSoup as bs
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options

base_url = 'https://www.saramin.co.kr'
headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.saramin.co.kr',
    'Referer': 'https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=47370025&recommend_ids=eJxdjsENQzEIQ6fpHYOB%2BNxBsv8Wza%2FUJKo4PRts2AG36jmAV7%2FZNEfFlPkfTn4FZ6ix16PCBxf2D0k%2FOExVZ1mpzp0dOTS0XZeCx7VK1xW1WkMb6blmI0Dj9QZrKRs9O7vOLYCR57YSfZLd0ci7KMT7DaU9%2BAHvZUQ%2F&view_type=list&gz=1&t_ref_content=general&t_ref=area_recruit&relayNonce=6086dd278acbb29270a8&immediately_apply_layer_open=n',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
session = req.Session()
res = session.get(base_url, headers=headers, verify=False)
cookies = dict(res.cookies)


def saram_crawler(id:str, url:str=None, display:str=None):
    file_name = f'../crawl/{id}/{id}.html'
    os.makedirs(f'../crawl/{id}', exist_ok=True) 
    if os.path.exists(file_name):
        logging.error(f'    Skip file : {file_name}')
        return
    data = {
        'rec_idx': id,
        'rec_seq': '2',
        'utm_source': '',
        'utm_medium': '',
        'utm_term': '',
        'utm_campaign': '',
        'view_type': 'list',
        't_ref': 'area_recruit',
        't_ref_content': 'general',
        't_ref_scnid': '902',
        'search_uuid': '',
        'refer': '',
        'searchType': '',
        'searchword': '',
        'ref_dp': 'SRI_050_VIEW_MTRX_RCT_NOINFO',
        'dpId': '',
        'recommendRecIdx': '',
    }
    res = req.post(f'{base_url}/zf_user/jobs/relay/view-ajax', cookies=cookies, headers=headers, data=data)
    if res.status_code != 200:
        logging.error(' error 발생')
        raise
    logging.info(f'crawling {id}')
    with open(file_name, 'wt', encoding='utf-8') as fs:
        fs.write(res.content.decode('utf-8'))
    sleep(5)
    get_iframe(id)


def get_iframe(id):
    file_name = f'../crawl/{id}/{id}.html'
    doc = None
    with open(file_name, 'rt', encoding='utf-8') as fs:
        doc = bs(fs.read(), 'html.parser')
    for iframe in doc.find_all('iframe'):
        try:
            src = base_url + iframe.get('src')
            file_name = f'../crawl/{id}/{hash(src)}'
            res = session.get(src, headers=headers, cookies=cookies, verify=False)
            bs(res.content, 'html.parser')
            with open(file_name, 'wt', encoding='utf-8') as fs:
                fs.write(res.content.decode('utf-8'))
            sleep(2)
        except:
            logging.error(f' get iframe fail:{file_name}')
    return True


if __name__=='__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.root.name=f"saramin_#{socket.gethostname()}"
    try:
        logging.root.name=f"saramin_#{os.environ['id']}"
    except:
        pass
    parser = argparse.ArgumentParser(
                    prog='saramin crawler',
                    description='saramin 구인목록을 크롤합니다.')
    parser.add_argument('-i', '--id')
    parser.add_argument('-u', '--url')
    parser.add_argument('-d', '--display')
    args = parser.parse_args()
    saram_crawler(args.id, args.url, args.display)
