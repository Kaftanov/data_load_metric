import logging
from loader import load_data
from merger import convert, create_frame
from cleaner import default_cleanup
import os
from datetime import datetime
import pandas as pd


CLEAN_FRAME_PATH = 'clean_frames_archive'
DEFAULT_SUFFIX = '_cleaned'
FINAL_PATH = 'data'

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='logs\\main.log')


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.makedirs('logs')
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    logging.info("__INIT__ Chain")
    print('__INIT__ Chain')
    load_data(type_=2)
    convert()
    frame = create_frame()
    frame = default_cleanup(frame)

    if not os.path.exists(CLEAN_FRAME_PATH):
        os.makedirs(CLEAN_FRAME_PATH)

    frame.to_csv(f"{CLEAN_FRAME_PATH}\\fats_df_{datetime.today().strftime('%m%d%Y')}{DEFAULT_SUFFIX}.csv", encoding='utf-8',
                 index=False)

    if not os.path.exists(FINAL_PATH):
        os.makedirs(FINAL_PATH)

    if len(os.listdir(CLEAN_FRAME_PATH)) > 1:
        data_frame = pd.DataFrame()
        for table in os.listdir(CLEAN_FRAME_PATH):
            data_frame = data_frame.append(pd.read_csv(os.path.join(CLEAN_FRAME_PATH, table)), sort=True)
        data_frame.to_csv(f"{FINAL_PATH}\\flats_data_{datetime.today().strftime('%m%d%Y')}.csv", index=False,
                          encoding='utf-8')
