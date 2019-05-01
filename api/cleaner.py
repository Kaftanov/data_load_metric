import pandas as pd
import ast
from pandas.io.json import json_normalize
import os


def extract_key(json_string, key):
    if type(json_string) == dict:
        return json_string[key]
    else:
        return eval(json_string)[key]


def flatten_json(d):
    if type(d) == dict:
        return d
    else:
        return ast.literal_eval(d)


def flatten_list_of_dicts(ld):
    return dict([(list(d.values())[1], list(d.values())[0]) for d in ast.literal_eval(ld)])


def convert_to_list(obj):
    if type(obj) == str:
        return eval(obj)
    else:
        return obj


def convert_to_str(obj):
    if type(obj) == str:
        return obj
    else:
        return str(obj)


def default_cleanup(frame):
    """

    :param frame: pd.DataFrame object from 'merger.py'
    :return:
    """
    local_frame = frame.copy()
    local_frame.dropna(axis=1, how='all', inplace=True)
    local_frame.drop(['added', 'addedTimestamp', 'bedsCount', 'categoriesIds', 'cianId', 'cianUserId',
                      'descriptionMinhash', 'descriptionWordsHighlighted', 'forDay', 'gaLabel', 'gaObjectType',
                      'jkUrl', 'modelVersion', 'objectGuid', 'platform', 'publishedUserId', 'specialty', 'userId',
                      'videos', 'photos', 'windowsViewType', 'withoutClientFee', 'adfoxParams', 'humanizedTimedelta',
                      'id', 'newbuildingVasPromotion', 'notes'], inplace=True, axis=1, errors="ignore")
    try:
        local_frame['allRoomsArea'].fillna('0', inplace=True)
    except KeyError:
        local_frame['totalArea'].fillna('0', inplace=True)
    local_frame['balconiesCount'] = local_frame['balconiesCount'].fillna(0).astype(int)

    local_frame['bargainTerms'].fillna('{"price": None, "currency": None, "deposit": None}', inplace=True)

    local_frame['flatPrice'] = local_frame['bargainTerms'].apply(extract_key, key='price')
    local_frame['flatPriceCurrency'] = local_frame['bargainTerms'].apply(extract_key, key='currency')
    local_frame['flatPriceDeposit'] = local_frame['bargainTerms'].apply(extract_key, key='deposit')
    local_frame.drop('bargainTerms', inplace=True, axis=1)

    local_frame['building'].fillna('{"buildYear": None, "materialType": None, "floorsCount": None, '
                                   '"passengerLiftsCount": None, "cargoLiftsCount": None}', inplace=True)

    local_frame['buildYear'] = local_frame['building'].apply(extract_key, key='buildYear')
    local_frame['buildMaterialType'] = local_frame['building'].apply(extract_key, key='materialType')
    local_frame['buildfloorsCount'] = local_frame['building'].apply(extract_key, key='floorsCount')
    local_frame['buildPassengerLiftsCount'] = local_frame['building'].apply(extract_key, key='passengerLiftsCount')
    local_frame['buildCargoLiftsCount'] = local_frame['building'].apply(extract_key, key='cargoLiftsCount')
    local_frame.drop('building', inplace=True, axis=1)

    local_frame['newbuilding'].fillna(False, inplace=True)
    local_frame.loc[local_frame['newbuilding'] != False, 'newbuilding'] = True
    local_frame.drop('newbuilding', inplace=True, axis=1)

    local_frame['user'].fillna("{}", inplace=True)
    agency_data = json_normalize(local_frame['user'].apply(flatten_json).tolist()).add_prefix('user.')
    agency_data['user.phoneNumbers'].fillna("[{'number': '0', 'countryCode': '+7'}]", inplace=True)
    local_frame['userAccountType'] = agency_data['user.accountType']
    local_frame['userAgencyName'] = agency_data['user.agencyName']
    local_frame['userAgentAvailabilityUserId'] = agency_data['user.agentAvailability.userId']
    local_frame['userPhoneNumber'] = agency_data['user.phoneNumbers'].apply(convert_to_list).apply(
        lambda x: x[0]['countryCode'] + x[0]['number'])
    local_frame['creationDate'] = pd.to_datetime(local_frame['creationDate'])
    local_frame.drop(['phones', 'user'], inplace=True, axis=1)
    return local_frame


def delete_files(folder_path):
    for file in os.listdir(folder_path):
        os.remove(os.path.join(folder_path, file))
