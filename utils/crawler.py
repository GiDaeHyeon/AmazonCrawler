import asyncio
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

    def parsing(self, resp: requests.Response) -> str:
        return self.parser(resp.text)


async def main() -> str:
    c = AsyncCrawler()
    target_url = "https://movie.naver.com/movie/point/af/list.naver?&page=1"
    html = await c.request(url=target_url)
    return html
