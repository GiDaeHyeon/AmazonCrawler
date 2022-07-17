import csv
import asyncio
from utils.logger import get_logger
from utils.crawler import AsyncCrawler
from datetime import datetime

logger = get_logger(__name__)
loop = asyncio.get_event_loop()
crawler = AsyncCrawler()


async def fetch_one_page(url: str) -> list:
    html = await crawler.request_parsing(url)

    if html is None:
        raise ConnectionError

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


async def save_review_data(page_num: int) -> None:
    base_url = 'https://movie.naver.com/movie/point/af/list.naver?&page={page_num}'
    header = ['idx', 'movie', 'score', 'content', 'writer', 'created_at']
    try:
        data = await fetch_one_page(base_url.format(page_num=page_num))
    except ConnectionError as E:
        logger.warning(f'{page_num} is Not Crawled')
    with open(f'./data/{page_num}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    logger.info(f"{page_num} is Crawled Successfully")


async def main() -> None:
    futures = [asyncio.ensure_future(save_review_data(page_num=page_num)) for page_num in range(1, 100)]
    await asyncio.gather(*futures)


if __name__ == '__main__':
    start_time = datetime.now()
    loop.run_until_complete(main())
    loop.close()
    logger.info("Done!!")
    logger.info(f"It took {datetime.now() - start_time}")
