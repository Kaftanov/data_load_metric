import requests
import logging
import csv
from bs4 import BeautifulSoup
from adds import ShortAdd
from time import sleep
from fake_useragent import UserAgent
import os
from tqdm import tqdm


def parse_card(house_card, type_):
    """

    :param type_: 'big' or 'small' type for card
    :param house_card: BeautifulSoup tag object
    :return:
    """
    short_ad = ShortAdd(source='cian')
    # get direct url
    if type_ == 'big':
        try:
            short_ad.title = house_card.find('div', {'class': 'c6e8ba5398--single_title--22TGT'}).text
        except AttributeError:
            short_ad.title = house_card.find('div', {'class': 'c6e8ba5398--title--39crr'}).text
            short_ad.sub_title = house_card.find('div', {'class': 'c6e8ba5398--subtitle--UTwbQ'}).text
        price_container = house_card.find('div', {'class': 'c6e8ba5398--price_flex_container--2kbcb'})
        short_ad.price = price_container.find('div', {'class': 'c6e8ba5398--header--1dF9r'}).text
        sub_items = price_container.find_all('div', 'c6e8ba5398--term--3kvtJ')
        if sub_items:
            short_ad.sub_items = [item.string for item in price_container.find_all('div', 'c6e8ba5398--term--3kvtJ')]
    elif type_ == 'small':
        title = house_card.find('div', {'class': 'c6e8ba5398--title--2CW78'})
        if title:
            short_ad.title = title.text
        sub_title = house_card.find('div', {'class': 'c6e8ba5398--lease-period--BAnbK'})
        if sub_title:
            short_ad.sub_title = sub_title.text
        price_container = house_card.find('div', {'class': 'c6e8ba5398--price-flex-container--36nYI'})
        price = price_container.find('div', {'class': 'c6e8ba5398--header--1df-X'})
        if price:
            short_ad.price = price.text
        sub_items = price_container.find_all('div', 'c6e8ba5398--term--3kvtJ')
        if sub_items:
            short_ad.sub_items = [item.string for item in price_container.find_all('div', 'c6e8ba5398--term--3kvtJ')]

    short_ad.url = house_card.find('a', {'class': 'c6e8ba5398--header--1Cu_4'})['href']

    holder = house_card.find('div', {'class': 'c6e8ba5398--name--3Tnuw'})
    if holder:
        short_ad.holder = holder.text

    short_description = house_card.find('div', {'class': 'c6e8ba5398--container--F3yyv'})
    if short_description:
        short_ad.short_description = short_description.text

    subway_station = house_card.find('div', {'class': 'c6e8ba5398--underground-name--3YjAi'})
    if subway_station:
        short_ad.subway_station = subway_station.text

    address = house_card.find('div', {'class': 'c6e8ba5398--address-links--1pHHO'}).find('span')
    if address:
        short_ad.address = address['content']
    return short_ad


def parse_page(page_content, page_number):
    """

    :param page_number: int, identifier for failed html file
    :param page_content: byte
    :return:
    """

    bs = BeautifulSoup(page_content, features="lxml")
    house_cards = bs.find_all('div', {'class': '_93444fe79c-card--2Jgih'})
    if not house_cards:
        with open(str(page_number) + 'content.html', "wb") as fd:
            fd.write(page_content)
    for house_card in house_cards:
        try:
            if 'c6e8ba5398--top3--2LNO_' in house_card.find('div')['class']:
                short_add = parse_card(house_card=house_card, type_='big')
            else:
                short_add = parse_card(house_card=house_card, type_='small')
            with open("data.csv", "a", encoding="utf-8") as fd:
                writer = csv.writer(fd, delimiter='\t', lineterminator='\n')
                writer.writerow(short_add.get_list_values())
        except Exception as error:
            logging.critical(error)
            with open(os.path.join('broken_files', str(page_number) + 'content.html', "wb")) as fd:
                fd.write(page_content)


def get_first_page():
    first_page_link = "https://www.cian.ru/snyat-kvartiru/"
    response = requests.get(first_page_link)
    parse_page(response.content, 0)


def run():
    # have a problem with first page
    # getting manually
    url_temp = 'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={}&region=1&type=4'
    with open("data.csv", "w", encoding="utf-8") as fd:
        writer = csv.writer(fd, delimiter='\t', lineterminator='\n')
        writer.writerow(ShortAdd.get_str_attributes())
    get_first_page()
    ua = UserAgent()
    session = requests.Session()
    session.headers.update({'User-Agent': ua.random})
    for page_index in tqdm(range(2, 10000)):
        response = session.get(url_temp.format(page_index))
        parse_page(page_content=response.content, page_number=page_index)
        sleep(5)


if __name__ == '__main__':
    run()
