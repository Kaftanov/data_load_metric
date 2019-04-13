import pandas as pd
import json
import os
from tqdm import tqdm
from datetime import datetime
import logging

from cleaner import default_cleanup

# COMMON DEFINES
DEFAULT_DIR_NAME = "downloads"
PROCESSED_FILES_DIR_NAME = "processed_jsons"

DEFAULT_PREFIX = 'flats_df_'
DEFAULT_SUFFIX = '_cleaned'

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename='logs\\merger.log')


def convert():
    for json_file in tqdm(os.listdir(DEFAULT_DIR_NAME)):
        with open(os.path.join(DEFAULT_DIR_NAME, json_file), "r") as fd:
            data = json.load(fd)
            if data["data"]["offersSerialized"]:
                logging.info("Using <offersSerialized>")
                json_data = json.dumps(data["data"]["offersSerialized"], indent=4)
            else:
                logging.info("Using <suggestOffersSerializedList>")
                json_data = json.dumps(data["data"]["suggestOffersSerializedList"], indent=4)
        with open(os.path.join(PROCESSED_FILES_DIR_NAME, json_file), "w") as fd:
            fd.write(json_data)


def create_frame():
    frame = pd.DataFrame()
    for json_file in tqdm(os.listdir(PROCESSED_FILES_DIR_NAME)):
        temp_df = pd.read_json(os.path.join(PROCESSED_FILES_DIR_NAME, json_file))
        logging.info(f"{json_file} -- {temp_df.shape}")
        frame = frame.append(temp_df, sort=True)
    frame.to_csv(f"{DEFAULT_PREFIX}{datetime.today().strftime('%m%d%Y')}.csv", encoding="utf-8", index=False)
    return frame


if __name__ == '__main__':

    if not os.path.exists(PROCESSED_FILES_DIR_NAME):
        os.makedirs(PROCESSED_FILES_DIR_NAME)
    convert()
    frame = create_frame()
    frame = default_cleanup(frame)
    frame.to_csv(f"{DEFAULT_PREFIX}{datetime.today().strftime('%m%d%Y')}{DEFAULT_SUFFIX}.csv", encoding='utf-8',
                 index=False)
