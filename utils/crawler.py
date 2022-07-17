import asyncio
import logging
import aiohttp

import requests
from fake_headers import Headers
from lxml import html


class AsyncCrawler:
    def __init__(self) -> None:
        self.headers = Headers(browser='chrome', headers=True)
        self.parser = html.fromstring
        self.loop = asyncio.get_event_loop()

    async def request_parsing(self, url: str) -> str:
        async with aiohttp.ClientSession(headers=self.headers.generate()) as session:
            async with session.get(url=url) as response:
                if response.status != 200:
                    return None
                else:
                    resp = await response.text()
        return self.parser(resp)


class Crawler:
    def __init__(self) -> None:
        self.headers = Headers(browser='chrome', headers=True)
        self.parser = html.fromstring

    def request(self, url: str) -> requests.Response:
        resp = requests.get(url=url, headers=self.headers.generate())
        if resp.status_code != 200:
            return None
        return resp

    def parsing(self, resp: requests.Response):
        return self.parser(resp.text)


async def main():
    c = AsyncCrawler()
    target_url = "https://movie.naver.com/movie/point/af/list.naver?&page=1"
    html = await c.request(url=target_url)
    return html

# Test
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    a_html = loop.run_until_complete(main())
    t = a_html.xpath('//*[@id="old_content"]/table/tbody')[0]
    a = t.findall('tr')
    td = a[0].findall('td')

    for idx, ll in enumerate(td):
        if idx == 0:  # 글 번호
            print(ll.text)
        elif idx == 1:  # 제목
            print(ll.find('a').text)  # 제목
            print(ll.find('div').find('em').text)  # 평점
            print(ll.xpath('text()')[3].strip())
        elif idx == 2:  # 작성자 및 작성일
            print(ll.find('a').text)  # 작성자
            print(ll.xpath('text()')[0])  # 작성일
