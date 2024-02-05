import pandas as pd
import orjson as json
from glob import glob


result = []
for file_name in glob('../result/*.json'):
    try:
        with open(file_name, 'rt', encoding='utf-8') as fs:
            result.append(json.loads(fs.read()))
    except:
        print(f'parse error:{file_name}')

df = pd.DataFrame(result)
df.to_csv('../result/saramin.csv', encoding='utf-8')
df.to_excel('../result/saramin.xlsx')


