import os
import requests
import wget
import multiprocessing
from bs4 import BeautifulSoup
from lxml import etree
from config import *


def get_page(url: str) -> bytes:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f'Could not fetch the page: {resp.status_code}: {resp.text}')
    return resp.content


def parse_page(page_content: bytes) -> BeautifulSoup:
    return BeautifulSoup(page_content, 'html.parser')


def get_and_parse_page(url: str) -> BeautifulSoup:
    return parse_page(get_page(url))


def get_anime_links(page: BeautifulSoup) -> list:
    dom = etree.HTML(str(page))
    return dom.xpath(r'//*[@id="flisttable"]/tbody/tr/td/a/@href')


def is_blacklisted(a_element: etree.Element) -> bool:
    text = a_element.xpath('strong/text()')[0]
    return any([blacklisted in text.lower() for blacklisted in FILE_TITLES_BLACKLIST])


def find_subtitle_download_for_anime(anime_page: BeautifulSoup) -> str | None:
    dom = etree.HTML(str(anime_page))
    all_links = dom.xpath(rf'//*[@id="flisttable"]/tbody/tr')
    for link_item in all_links:
        subtitle_page_a = link_item.xpath(r'td[1]/a')[0]
        if not is_blacklisted(subtitle_page_a):
            url = subtitle_page_a.xpath('@href')[0]
            return f'{BASE_URL}/{url}'
    print('Skipped downloading')
    return None


def download(url: str, output_folder: str):
    wget.download(url, out=output_folder)


def download_for_anime(link: str):
    sort_by_filesize_param = '&sort=size&order=desc'
    download_link = find_subtitle_download_for_anime(get_and_parse_page(BASE_URL + link + sort_by_filesize_param))
    if download_link is not None:
        download(download_link, SUBTITLE_ZIP_OUTPUT)


def preprare_folder(folder: str):
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass


def main():
    preprare_folder(SUBTITLE_ZIP_OUTPUT)
    page = get_and_parse_page(PAGE_URL)
    links = get_anime_links(page)
    if MULTITHREAD:
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        pool.map(download_for_anime, links)
        pool.close()
        pool.join()
    else:
        for link in links:
            download_for_anime(link)
    

if __name__ == '__main__':
    main()
