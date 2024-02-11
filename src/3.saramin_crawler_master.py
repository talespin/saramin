import pandas as pd
from multiprocessing import Pool



def main():
    items = pd.read_excel('../list/saramin.xlsx').to_dict('records')
    lst = []
    for item in items:
        pgm = f'rsh crawler{server} \'export DISPLAY={os.environ["DISPLAY"]};cd /mnt/work/saramin/src;/usr/share/python-3.11/bin/python 3.saramin_crawler_one.py -i {id} -u "{url}" -d "{display}"\''
        lst.append(pgm)
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
