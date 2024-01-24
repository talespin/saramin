def saram_crawler(list_file:str, overwrite:bool = False):
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
            logging.info(f'    Skip exists file : {file_name}'
            continue
        while True:
            logging.info(f'    Crawling {file_name} ....')
            res = session.get(f'https://www.saramin.co.kr/zf_user/jobs/relay/view?&rec_idx={id}', headers=headers, verify=False, cookies=cookies)
            if res.status_code == 200: break
            sleep(10)


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    parser = argparse.ArgumentParser(
                    prog='saramin crawler',
                    description='saramin 구인목록을 크롤합니다.')
    parser.add_argument('-l', '--list')
    parser.add_argument('-o', '--overwrite', default=False)
    args = parser.parse_args()
    saram_crawler(args.list, args.overwrite)
