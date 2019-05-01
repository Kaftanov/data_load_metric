import logging
from loader import load_data
from merger import convert, create_frame
from cleaner import default_cleanup, delete_files
import os
from datetime import datetime
import pandas as pd


CLEAN_FRAME_PATH = 'clean_frames_archive'
DEFAULT_SUFFIX = '_cleaned'
FINAL_PATH = 'data'

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='logs\\main.log')


def get_proxy(file_path):
    data = pd.read_csv(file_path)
    for proxy in data.iterrows():
        yield {"http": f"{proxy[1]['address']}:{proxy[1]['port']}"}


if __name__ == '__main__':
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    else:
        if len(os.listdir('downloads')) > 1:
            delete_files('downloads')
    
    logging.info("__INIT__ Chain")
    print('__INIT__ Chain')
    page_number = load_data(protocol="http", type_=2, start_=1)
    for proxy in get_proxy("proxy.csv"):
        print(f"Processing: {page_number} <~~")
        page_number = load_data(protocol="http", proxy=proxy, type_=2, start_=page_number)
    """
    convert()
    frame = create_frame()
    frame = default_cleanup(frame)

    if not os.path.exists(CLEAN_FRAME_PATH):
        os.makedirs(CLEAN_FRAME_PATH)

    frame.to_csv(f"{CLEAN_FRAME_PATH}\\fats_df_{datetime.today().strftime('%m%d%Y_%H%M%S')}{DEFAULT_SUFFIX}.csv",
                 encoding='utf-8', index=False)

    if not os.path.exists(FINAL_PATH):
        os.makedirs(FINAL_PATH)

    if len(os.listdir(CLEAN_FRAME_PATH)) > 1:
        data_frame = pd.DataFrame()
        for table in os.listdir(CLEAN_FRAME_PATH):
            data_frame = data_frame.append(pd.read_csv(os.path.join(CLEAN_FRAME_PATH, table)), sort=True)
        data_frame.to_csv(f"{FINAL_PATH}\\flats_data_{datetime.today().strftime('%m%d%Y_%H%M%S')}.csv", index=False,
                          encoding='utf-8')
