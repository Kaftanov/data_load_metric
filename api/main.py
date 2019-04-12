import logging
import requests
from time import sleep
from tqdm import tqdm
import json
from random import random, uniform


logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='mylog.log')

url = "https://api.cian.ru/search-offers/v2/search-offers-desktop/"

payload = '{\"jsonQuery\":{\"region\":{\"type\":\"terms\",\"value\":[1]},\"_type\":\"flatrent\",\"engine_version\":{' \
          '\"type\":\"term\",\"value\":2},\"for_day\":{\"type\":\"term\",\"value\":\"!1\"},\"page\":{' \
          '\"type\":\"term\",\"value\":%s}}} '

room_filter_payload = "{\"jsonQuery\":{\"_type\":\"flatrent\",\"room\":{\"type\":\"terms\",\"value\":[1,2,3]}," \
                      "\"for_day\":{\"type\":\"term\",\"value\":\"!1\"},\"region\":{\"type\":\"terms\",\"value\":[" \
                      "1]},\"engine_version\":{\"type\":\"term\",\"value\":2},\"page\":{\"type\":\"term\"," \
                      "\"value\":%s}}}"

headers = {
    'Content-Type': "text/plain;charset=UTF-8",
    'DNT': "1",
    'Origin': "https://www.cian.ru",
    'Referer': "https://www.cian.ru/snyat-kvartiru/",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    'cache-control': "no-cache"
    }

for page in tqdm(range(350, 2000)):
    try:
        response = json.loads(requests.request("POST", url, data=room_filter_payload % page, headers=headers).content)
        if response['status'] == 'ok':
            with open(f"downloads\\data_page_{page}.json", "w") as fd:
                fd.write(json.dumps(response, indent=4))
        else:
            logging.critical("Error from server")
            logging.critical(response['status'])
        logging.info(f"Page number {page} completed")
        sleep(uniform(5, 10))
    except Exception as error:
        logging.critical(str(error))
        print(f"\n\nPage number {page} failed")
        break

