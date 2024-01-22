import os
import urllib3
from urllib.parse import urlencode
import logging
import pandas as pd
import requests as req
from time import sleep
from bs4 import BeautifulSoup as bs
import json
import math

#https://curlconverter.com/


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def saramin_list():
    logging.info('start crawl list saramin')
    #지역별 코드
    with open('./local_cd.json', encoding='UTF8') as json_file:
        local_cd = json.load(json_file)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        "Connection": 'keep-alive',
        'Content-type': 'application/json',
        "Cookie": 'PHPSESSID=v93t59kf5vsn1k6dbkr39mvg4htibbvnv14e4unb1em9u1jl11; PCID=17052286096056809239551; _fwb=23i37i1RqaF6cuMS8m6cSf.1705228609175; ab180ClientId=8c1a8144-001d-4f69-a515-9e204d6fd27e; _gid=GA1.3.1984738359.1705228609; __gads=ID=c3c8f756762a190b:T=1705228611:RT=1705229256:S=ALNI_MZt2ZYrKBstqxv6EKIdUrX7ZkQdaA; __gpi=UID=00000cd9fd590788:T=1705228611:RT=1705229256:S=ALNI_MZOotiYSE8WHIqrHUZaqQ0NxMxwEA; RSRVID=web18|ZaO7+|ZaO5R; wcs_bt=s_1d3a45fb0bfe:1705229299; airbridge_session=%7B%22id%22%3A%2297ed3dcf-ccbe-46bf-93f4-a635dafd4e8a%22%2C%22timeout%22%3A1800000%2C%22start%22%3A1705228609709%2C%22end%22%3A1705229299693%7D; _ga=GA1.1.1777098376.1705228609; _ga_GR2XRGQ0FK=GS1.1.1705228609.1.1.1705229299.15.0.0; cto_bundle=vvgRR19PUkRSYXNyenU5Vmo0ZkduYUFnWVdIZVptNWxpaXI3TThRWVNvZU85UXU0OGhTJTJCSEZIQ2JzRWZSM2pEUlZYJTJCTW9vcmlDSnZvM2Q4ckZ0TzdsVlJIZVdFMWRQVWRWckklMkJwS0lIdUZ5T3NaODlyM1NoNFlOVUJuckIlMkJOQUJTWmJ1V3NpVUMlMkZHdGFzeEN4Zkp3MTdMbkJrM0tkVHVlc2s3QVclMkIxYVJNT0wzM0dRUWwlMkZtdXhhOHMzMGtuV1RocHZQQWpXUU9yRllSVm1Oa05BTjJDMDJRV3clM0QlM0Q; _gali=sri_wrap',
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
    #세션 및 쿠키생성
    session = req.Session()
    base_url = 'https://www.saramin.co.kr'
    res = session.get(base_url, headers=headers, verify=False)
    cookies = dict(res.cookies)
    #목록조회
    page = 1
    page_count = 100
    doc = bs(res.content, 'html.parser')
    total_count = int(doc.select('.total_count em')[0].text.replace(',', ''))
    total_page = math.ceil(total_count / page_count)
    items = []
    while True:
        logging.info(f"    page={page} / {total_page}")
        data = {
            'page': f'{page}',
            'loc_mcd': local_cd[0]['data_code'],
            'page_count': f'{page_count}',
        }
        logging.debug(str(data))
        if os.path.exists(f'../list/{page}'):
            with open(f'../list/{page}','rb') as fs:
                doc = bs(fs.read(), 'html.parser')
        else:
            sleep(5)
            res = session.get(f'{base_url}/zf_user/jobs/list/domestic/{urlencode(data)}', cookies=cookies, headers=headers, verify=False)
            with open(f'../list/{page}','rb') as fs:
                fs.write(res.content)
            doc = bs(res.content, 'html.parser')
        page = page+1
        if page > total_page: break
        _items = doc.select('.list_body div[id^="rec"]')
        for item in _items:
            a = item.find(class_='job_tit').find('a')
            url = base_url + a.get('href')
            job_tit = a.get('title')
            job_meta = [x.text.strip() for x in item.select('.job_sector span')]
            list_info = [x.text.strip() for x in item.select('.recruit_info li')]
            items.append(dict(id=item.get('id'), url=url, job_tit=job_tit, job_meta=job_meta, list_info=list_info))
    logging.info('crawl list saramin complete')
    #리스트 크롤완료
    logging.info('make list file processing...')
    os.makedirs('../list', exist_ok=True)
    pd.DataFrame(items).to_excel('../list/saramin.xlsx', index=False)
    logging.info('complete!!!')


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.out)
    saramin_list()