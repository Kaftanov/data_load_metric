import logging.config
import os
import json

from selenium import webdriver
from time import sleep


def get_chrome_options(incognito_mode=False):
    custom_config = load_json_config("browser_config.json")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")

    if not os.path.exists(custom_config["browser"]["chrome"]["download_path"]):
        os.makedirs(custom_config["browser"]["chrome"]["download_path"])

    chrome_options.add_experimental_option("prefs", custom_config["browser"]["chrome"]["pref"])
    if incognito_mode:
        chrome_options.add_argument("--incognito")
    return chrome_options


def load_json_config(path):
    with open(path, "r") as fd:
        return json.load(fd)


if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger("context")
    custom_config = load_json_config("browser_config.json")
    driver = webdriver.Chrome("drivers/chromedriver_win32.exe",
                              chrome_options=get_chrome_options(incognito_mode=False))
    driver.get("https://www.cian.ru/")
    sleep(10000)

