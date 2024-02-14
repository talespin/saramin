import pandas as pd
from time import sleep
from os.path import exists
from datetime import datetime

df = pd.read_excel('../list/saramin.xlsx')
df['exists'] = False
while True:
    df['exists'] = df.apply(lambda x:x['exists'] if x['exists'] else exists(f'../crawl/{x["id"]}/{x["id"]}.html'), axis=1)
    print(f'{datetime.now()}  남은크롤갯수 : {len(df[df["exists"]==False])}  / {len(df)}')
    sleep(60)

