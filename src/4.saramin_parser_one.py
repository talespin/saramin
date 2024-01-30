#!/usr/bin/python
"""
:filename: 4.saramin_parser_one.py
:author: 최종환
:last update: 2024.01.11
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.11     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    saramin crawl 된 html을  result 폴더에 각각 파싱하여 json 으로 변환한다.
 
"""
import os
import sys
import logging
import orjson as json
from glob import glob
from datetime import datetime
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool


def parser(file_name:str) -> None:
    logging.info(f' parse : {file_name}')
    if not os.path.exists(file_name): return
    id = os.path.basename(file_name).split('.')[0]
    json_file = f'../result/{id}.json'
    if os.path.exists(json_file): return
    doc = None
    with open(file_name, 'rt', encoding='utf-8') as fs:
        doc = bs(fs.read(), 'html.parser')
    job_tile = doc.find('h1', {'class':'tit_job'}).text.strip()
    _summary = doc.find('div', {'class':'jv_cont jv_summary'})
    dct_summary = {}
    for dt, dd in zip(_summary.find_all('dt'), _summary.find_all('dd')):
        dct_summary.update({'summary:'+dt.text.strip():dd.text.strip()})
    _jv_cont = doc.find('div', {'class':'jv_cont jv_location'})
    company_name = _jv_cont.get("data-company-name")
    company_address =  _jv_cont.get("data-address")
    address = doc.find('address', {'class':'address'}).text.strip()
    _info_period = doc.find('dl', {'class':'info_period'})
    dct_period = {}
    for dt, dd in zip(_info_period.find_all('dt'), _info_period.find_all('dd')):
        dct_period.udpate({'period:'+dt.text.strip():dd.text.strip()})
    result = dict(id=id, job_title=job_tile, company_name=company_name, company_address=company_address)
    result.update(dct_summary)
    result.update(dct_period)    


def main():
    logging.info('start parse html')
    logging.info(datetime.now())
    file_names = glob('../crawl/*.html')
    pool = Pool(4)
    pool.map_async(parser, file_names)
    pool.join()
    pool.close()
    logging.info('end parse html')
    logging.info(datetime.now())


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.root.name = 'saramin_parser_one'
    main()

