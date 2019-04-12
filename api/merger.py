import pandas as pd
import json
import os
from tqdm import tqdm


def convert():
    for json_file in tqdm(os.listdir("downloads")):
        with open(os.path.join("downloads", json_file), "r") as fd:
            data = json.load(fd)
            print(len(data))
            if data["data"]["offersSerialized"]:
                json_data = json.dumps(data["data"]["offersSerialized"], indent=4)
            else:
                json_data = json.dumps(data["data"]["suggestOffersSerializedList"], indent=4)
        with open(os.path.join("processed_jsons", json_file), "w") as fd:
            fd.write(json_data)


convert()

flats_df = pd.DataFrame()

for json_file in os.listdir("processed_jsons"):
    temp_df = pd.read_json(os.path.join("processed_jsons", json_file))
    print(json_file, temp_df.shape)
    flats_df = flats_df.append(temp_df, sort=True)

flats_df.to_csv("flats_df.csv", encoding="utf-8", index=False)
