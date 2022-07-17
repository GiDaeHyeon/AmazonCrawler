import csv
from datetime import datetime
from utils.logger import get_logger
from utils.crawler import Crawler

logger = get_logger(__name__)
crawler = Crawler()


def fetch_one_page(url: str):
    resp = crawler.request(url)
    if resp is None:
        raise ConnectionError
    html = crawler.parsing(resp)
    table = html.xpath('//*[@id="old_content"]/table/tbody')[0]
    trs = table.findall('tr')

    page_data = []
    for tr in trs:
        row = []
        tds = tr.findall('td')
        for idx, td in enumerate(tds):
            if idx == 0:
                row.append(td.text)  # 글 번호
            elif idx == 1:
                row.append(td.find('a').text)  # 제목
                row.append(td.find('div').find('em').text)  # 평점
                row.append(td.xpath('text()')[3].strip())  # 내용
            elif idx == 2:
                row.append(td.find('a').text)  # 작성자
                row.append(td.xpath('text()')[0])  # 작성일
        page_data.append(row)
    return page_data


def save_review_data(page_num: int):
    base_url = 'https://movie.naver.com/movie/point/af/list.naver?&page={page_num}'
    header = ['idx', 'movie', 'score', 'content', 'writer', 'created_at']
    try:
        data = fetch_one_page(base_url.format(page_num=page_num))
    except ConnectionError as E:
        logger.error(f'{page_num} is Not Crawled')
    with open(f'./data/{page_num}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    logger.info(f"{page_num} is Crawled Successfully")


def main():
    for page_num in range(1, 100):
        save_review_data(page_num=page_num)


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    logger.info("Done!!")
    logger.info(f"It took {datetime.now() - start_time}")
