import pandas as pd
import json
import os
from tqdm import tqdm
from datetime import datetime
import logging
from cleaner import delete_files


if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename='logs\\merger.log')


def convert(input_path='downloads', output_path='processed_jsons'):
    """

    :param input_path:
    :param output_path:
    :return:
    """
    if not os.path.exists(input_path):
        raise Exception("Missing <json_files_path> folder")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        if len(os.listdir(output_path)) > 1:
            delete_files(output_path)
    for json_file in tqdm(os.listdir(input_path)):
        with open(os.path.join(input_path, json_file), "r") as fd:
            data = json.load(fd)
            if data["data"]["offersSerialized"]:
                logging.info("Using <offersSerialized>")
                json_data = json.dumps(data["data"]["offersSerialized"], indent=4)
            else:
                logging.info("Using <suggestOffersSerializedList>")
                json_data = json.dumps(data["data"]["suggestOffersSerializedList"], indent=4)
        with open(os.path.join(output_path, json_file), "w") as fd:
            fd.write(json_data)


def create_frame(input_path='processed_jsons', output_path='source_frames_archive', file_prefix='flats_df_'):
    """

    :param input_path:
    :param output_path:
    :param file_prefix:
    :return:
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    frame = pd.DataFrame()
    for json_file in tqdm(os.listdir(input_path)):
        temp_df = pd.read_json(os.path.join(input_path, json_file))
        logging.info(f"{json_file} -- {temp_df.shape}")
        frame = frame.append(temp_df, sort=True)
    frame.to_csv(f"{output_path}\\{file_prefix}{datetime.today().strftime('%m%d%Y_%H%M%S')}.csv",
                 encoding="utf-8", index=False)
    return frame
