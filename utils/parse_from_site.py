import aiohttp
from loguru import logger

from loader import url_for_channels, url_for_categories, db
from database.models import Tgchannelscategories, TgChannels
from pprint import pprint
import asyncio
from bs4 import BeautifulSoup
import re
import random


headers = {
        'Host': 'teletarget.com',
        'User-Agent': ''
    }

list_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
                    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.432'
                    '2; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)',
                    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTM'
                    'L, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1']



async def get_channel_categories():
    list_categories = []
    await db.initial()
    async with aiohttp.ClientSession() as session:
        headers['User-Agent'] = list_user_agents[random.randint(0, len(list_user_agents) - 1)]
        pprint(headers)
        async with session.get(url=url_for_categories, headers=headers) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            pprint(soup.find('div', class_='list-group list-group-transparent mb-3'))
            result_data = soup.find('div', class_='list-group list-group-transparent mb-3')
            if result_data:
                for i_elem in result_data.find_all('a', class_='list-group-item list-group-item-action d-flex align-items-center'):
                    category = re.search(pattern=r'href="(/[^"]+)"',
                                         string=str(i_elem)).group().split('"')[1].split('/')[2]
                    if await db.get_row(Tgchannelscategories, category_name=category):
                        ...
                    else:
                        list_categories.append(Tgchannelscategories(category_name=category))
    if list_categories:
        await db.add_rows(list_categories)



async def parse_from_site():
    await db.initial()
    list_for_add = []
    async with aiohttp.ClientSession() as session:
        for i_elem in await db.get_row(Tgchannelscategories, to_many=True):
            current_page = 0
            category = i_elem.category_name
            while True:
                try:
                    current_page += 1
                    headers['User-Agent'] = list_user_agents[random.randint(0, len(list_user_agents) - 1)]
                    logger.debug(f'HEADERS ====== {headers}')
                    async with session.get(url=url_for_channels.format(category=category,
                                                                       num=current_page), headers=headers) as response:
                        if response.status == 404:
                            break
                        text = await response.text()
                        soup = BeautifulSoup(text, "html.parser")
                        if soup.find_all('tr', class_='offer bg-tabler-lt'):
                            result = soup.find_all('tr', class_='offer bg-tabler-lt')
                            logger.debug(f'LENGTH ====== {len(result)}')
                        else:
                            result = soup.find_all('tr', class_='offer')
                            logger.debug(f'LENGTH ====== {len(result)}')
                        for i_channel in result:
                            channel_name = i_channel.find('a', class_='channel_title').text
                            channel_image = f'https://teletarget.com{str(i_channel.find('div', class_='avatar '
                                 'd-block rounded-circle')).split('url(')[1].split(')">')[0]}'
                            channel_href = str(i_channel.find('a',
                              class_='channel_title')).split('href="')[1].split('">')[0].split('" ')[0]
                            subscribers_count = str(i_channel.find_all('td',
                                           class_='text-center')[3].text.replace('\n', '').replace('\xa0', '')).strip()
                            if subscribers_count:
                                subscribers_count = int(subscribers_count)
                            link_channel = 'https://teletarget.com{}'.format(channel_href)

                            async with session.get(url=link_channel, headers=headers) as response_2:
                                text_2 = await response_2.text()
                                soup2 = BeautifulSoup(text_2, "html.parser")
                                link_channel = soup2.find('div', class_='d-grid gap-1')
                                link_channel = str(link_channel.find_all('a')[0]).split('href="')[1].split('">')[0]
                            if not await db.get_row(TgChannels, tg_link=link_channel):
                                list_for_add.append(TgChannels(tg_channel_name=channel_name,
                                                               channel_photo=channel_image,
                                                               subscribers_count=subscribers_count,
                                                               tg_link=link_channel))
                    await asyncio.sleep(5)
                except Exception as exc:
                    logger.exception(exc)
                    break
        if list_for_add:
            await db.add_rows(list_for_add)


if __name__ == '__main__':
    asyncio.run(parse_from_site())
    #asyncio.run(get_channel_categories())
