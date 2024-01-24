#!/usr/bin/python
"""
:filename: 3.saramin_crawler.py
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
import urllib3
import logging
import argparse
import pandas as pd
import requests as req
from random import random
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def saram_crawler(list_file:str, overwrite:bool = False):
    os.makedirs('../crawl', exist_ok=True) 
    if not os.path.exists(list_file):
        print('File not found:' + os.path.abspath(list_file))
        return
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        "Connection": 'keep-alive',
        "Host": 'www.saramin.co.kr',
        "Referer": 'https://www.saramin.co.kr/zf_user/jobs/list/domestic',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": '?0',
        'sec-ch-ua-platform': "macOS",
    }
    params = {
        'view_type': 'list',
        'rec_idx': 'id',
        'location': 'ts',
        'searchType': 'search',
        'paid_fl': 'n',
        'inner_source': 'saramin',
        'inner_medium': 'pattern',
        'inner_campaign': 'SRI_050_ARA_MTRX_RCT',
        'inner_term': '1',
    }
    #세션 및 쿠키생성
    session = req.Session()
    base_url = 'https://www.saramin.co.kr'
    res = session.get(base_url, headers=headers, verify=False)
    cookies = dict(res.cookies)
    items = pd.read_json(list_file).to_dict('records')
    for item in items:
        id = item['id']
        file_name = f'../crawl/{id}/{id}.html'
        if os.path.exists(file_name):
            logging.info(f'    Skip exists file : {file_name}')
            continue
        while True:
            logging.info(f'    Crawling {file_name} ....')
            params.update({'rec_idx':id})
            res = session.get(f'{base_url}/zf_user/jobs/relay/view', params=params, headers=headers, verify=False, cookies=cookies)
            sleep(5)
            if res.status_code == 200: break
            sleep(10)



if __name__=='__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    parser = argparse.ArgumentParser(
                    prog='saramin crawler',
                    description='saramin 구인목록을 크롤합니다.')
    parser.add_argument('-l', '--list')
    parser.add_argument('-o', '--overwrite', default=False)
    args = parser.parse_args()
    saram_crawler(args.list, args.overwrite)
