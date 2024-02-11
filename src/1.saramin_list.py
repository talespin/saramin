#!/usr/bin/python
"""
:filename: 1.saramin_list.py
:author: 최종환
:last update: 2024.01.20
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.20     bum        최초생성
    ============== ========== ====================================
 
:desc:
    saramin site 의 지역별 채용정보 크롤 목록 생성
 
"""
import os
import sys
import json
import math
import urllib3
import logging
import pandas as pd
import requests as req
from glob import glob
from time import sleep
from urllib.parse import urlencode
from bs4 import BeautifulSoup as bs


def saramin_list():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.root.name='saramin_list'
    ip = None
    while True:
        ip = input('>>>크롤작업을 새로 시작하려면 Y  이어서 하려면 N 를 입력하세요\n')
        if ip in ['Y','N']: break
    if ip == 'Y': [os.remove(x) for x in glob('../list/*')]
    logging.info('start crawl list saramin')
    #지역별 코드
    #with open('./local_cd.json', encoding='UTF8') as json_file:
    #    local_cd = json.load(json_file)		
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        "Connection": 'keep-alive',
        'Content-type': 'application/json',
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
        'page': '1',
        'loc_mcd': '101000',
        'search_optional_item': 'n',
        'search_done': 'y',
        'panel_count': 'y',
        'preview': 'y',
        'isAjaxRequest': '1',
        'page_count': '100',
        'sort': 'RL',
        'type': 'domestic',
        'is_param': '1',
        'isSearchResultEmpty': '1',
        'isSectionHome': '0',
        'searchParamCount': '1',
        'tab': 'domestic',
    }
    #세션 및 쿠키생성
    page_count = 100
    session = req.Session()
    base_url = 'https://www.saramin.co.kr'
    res = session.get(base_url, headers=headers, verify=False)
    cookies = dict(res.cookies)
    #국내지역 지역별 데이터 건수 구하기
    url = f'{base_url}/zf_user/jobs/list/domestic'	
    res = req.get(url, headers=headers, cookies=cookies, verify=False)
    doc = bs(res.content, 'html.parser')
    scripts = doc.find_all('script')
    script = str([x for x in scripts if str(x).find('area_1depth_count') >= 0][0])
    ss = [x.strip() for x in script.split('\n') if x.strip().startswith("'options'")][0]
    js_cnt = json.loads(ss.split('//')[0][:-3][15:])
    area_cnt = []
    for _domestic in js_cnt['area_1depth_domestic_text']:
        print(_domestic, js_cnt['area_1depth_domestic_text'][_domestic], js_cnt['area_1depth_count'][_domestic])
        area_cnt.append(dict(id=_domestic, name=js_cnt['area_1depth_domestic_text'][_domestic], cnt=js_cnt['area_1depth_count'][_domestic], page_size=math.ceil(int(js_cnt['area_1depth_count'][_domestic])/page_count)))
    #지역별 페이지 크롤
    for area in area_cnt:
        params.update({'loc_mcd':area['id']})
        for page in range(1, area['page_size']+1):
            file_name = f'../list/' + area['id'] + f'_{page}.page'
            params.update({'page':page})
            if os.path.exists(file_name):
                logging.info(f'    Skip exists file: {file_name}')
                continue
            logging.info(f'crawl {area["name"]} {page}/{area["page_size"]}')
            sleep(5)
            res = session.get(f'{base_url}/zf_user/jobs/list/domestic', params=params, cookies=cookies, headers=headers)
            with open(file_name, 'wt', encoding='utf-8') as fs:
                fs.write(res.content.decode('utf-8'))
    logging.info('crawl list saramin complete')
    #리스트 크롤완료
    logging.info('리스트 생성을 시작합니다.')
    result = []
    for file_name in  [x for x in glob(f'../list/*_*.page') if not x.endswith('.json')]:
        try:     
            with open(file_name, 'rt', encoding='utf-8') as fs:
                doc = bs(fs.read(), 'html.parser')
            items = doc.find('section',{'class':'list_recruiting'}).find_all('div',{'class':'list_item'})
            id, company_name, title, sector, work_place, career, education, end_dt = '', '', '', '', '' ,'' ,'' ,''
            for item in items:
                id = item.get('id')
                company_name = item.find('div',{'class':'company_nm'}).text.strip().split('\n')[0]
                tilte = item.find('div',{'class':'job_tit'}).find('a').get('title')
                sector = [x.text.strip() for x in items[2].find('span',{'class':'job_sector'}).find_all('span')]
                work_place = item.find('p',{'class':'work_place'}).text.strip()
                career = item.find('p',{'class':'career'}).text.strip()
                education = item.find('p',{'class':'education'}).text.strip()
                end_dt = item.find('p',{'class':'support_detail'}).find('span',{'class':'date'}).text.strip()
                result.append(dict(id=id, title=title, company_name=company_name, sector=sector, work_place=work_place, career=career, education=education, end_dt=end_dt))
        except:
            logging.error(f'error file : {file_name}')
            raise
    logging.info('make list file processing...')
    os.makedirs('../list', exist_ok=True)
    pd.DataFrame(result).to_excel('../list/saramin.xlsx', index=False)
    logging.info('complete!!!')


if __name__=='__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    saramin_list()
