import logging
from loader import load_data
from merger import convert, create_frame
from cleaner import default_cleanup
import os
from datetime import datetime


CLEAN_FRAME_PATH = 'clean_frames_archive'
DEFAULT_SUFFIX = '_cleaned'

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='logs\\main.log')


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.makedirs('logs')
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    logging.info("__INIT__ Process")
    print('__INIT__ Process')
    load_data(type_=2)
    convert()
    frame = create_frame()
    frame = default_cleanup(frame)

    if not os.path.exists(CLEAN_FRAME_PATH):
        os.makedirs(CLEAN_FRAME_PATH)

    frame.to_csv(f"{CLEAN_FRAME_PATH}\\fats_df_{datetime.today().strftime('%m%d%Y')}{DEFAULT_SUFFIX}.csv", encoding='utf-8',
                 index=False)
