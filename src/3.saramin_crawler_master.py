#!/usr/bin/python
"""
:filename: 3.saramin_crawler_master.py
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
import urllib3
import pandas as pd
from multiprocessing import Pool


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    display = os.environ["DISPLAY"]
    #items = pd.read_excel('../list/saramin.xlsx').to_dict('records')
    items = pd.read_csv('../list/saramin.csv').to_dict('records')
    lst = []
    for i, item in enumerate(items):
        id, url = item['id'], ''
        if os.path.exists(f'../crawl/{id}/{id}.html'): continue
        server = (i % 5) +1
        pgm = f'rsh crawler{server} \'export DISPLAY={display};cd /mnt/work/saramin/src;/usr/share/python-3.11/bin/python 3.saramin_crawler_one.py -i {id} -u "{url}" -d "{display}"\''
        lst.append(pgm)
    print(f'total count:{len(items)},  exists count:{len(items) - len(lst)}, target count:{len(lst)}')
    print(f'crawl start')
    pool = Pool(10)
    pool.map_async(subprocess, lst)
    pool.close()
    pool.join()
    pool = None


def subprocess(pgm):
    p = os.popen(pgm)
    #sleep(40)
    print(p.read())


if __name__=='__main__':
    main()
