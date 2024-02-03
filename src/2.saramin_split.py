#!/usr/bin/python
"""
:filename: 2.saramin_split.py
:author: 최종환
:last update: 2024.01.20
 
:CHANGELOG:
    ============== ========== ====================================
    수정일            수정자        수정내용
    ============== ========== ====================================
    2024.01.20     최종환        최초생성
    ============== ========== ====================================
 
:desc:
    saramin site 의 체용정보 목록을 입력하는 숫자에 맞춰서 나눈다
 
"""
import os
import sys
import math
import logging
import pandas as pd


def main():
    split_cnt = int(input("\r\n\r\n몇개의 파일로 나눌까요?\r\n(숫자만입력해주세요)"))
    if not os.path.exists('../list/saramin.xlsx'):
        logging.info(os.path.abspath('../list/saramin.xlsx') + ' 파일이 없습니다. saramin_list.py 를 실행해서 먼저 리스트파일을 생성하세요')
        return
    df = pd.read_excel('../list/saramin.xlsx').drop_duplicates().reset_index(drop=True)
    if len(df) < split_cnt:
        logging.info('건수보다 나누려는 수가 큽니다.')
        return
    page_cnt = math.ceil(len(df) / split_cnt)
    for cnt in range(0, split_cnt):
        df[cnt *page_cnt:(cnt+1)*page_cnt].to_json(f'../list/saramin_{cnt+1}.json', orient='records', force_ascii=False)



if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.root.name='saramin_split')
    main()

