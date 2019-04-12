import json


class Add:
    # general
    totalArea: float = 0.0
    fullUrl: str = ''
    title: str = ''
    roomsCount: int = 0
    price: float = 0.0
    paymentPeriod: str = ''
    leaseTermType: str = ''
    deposit: str = ''
    currency: str = ''
    isAuction: bool = False
    isTop3: bool = False

    creationDate: str = ''  # convert to datetime object
    isApartments: bool = False
    description: str = ''
    isRentByParts: bool = False
    offerType: str = ''
    isPaid: bool = False
    garage = None  # I don't know the type
    phones_number: str = ''
    dealType: str = ''
    flatType: str = ''
    agencyName: str = ''
    isAgent: bool = False

    # location
    location_id: int = 0
    location_name: str = ''
    okrug_id: int = 0
    okrug_name: str = ''
    raion_id: int = 0
    raion_name: str = ''
    underground_id: int = 0
    underground_name: str = ''
    street_id: int = 0
    street_name: str = ''
    house_id: int = 0
    house_name: str = ''

    location_user_input = ''
    # coordinates
    lng: float = 0.0
    lat: float = 0.0
    # building
    buildYear: int
    accessType = None  # I don't know the type
    deadline = None  # I don't know the type
    heatingType = None
    materialType = None
    floorsCount: int = 0
    passengerLiftsCount: int = 0
    cargoLiftsCount: int = 0

    # about builder
    isFromBuilder: bool
    isFromDeveloper: bool
    isFromSeller: bool
    builder_name: str = ''

    def __init__(self):
        self.source = 'CIAN'


def parse_json(json_object):
    """

    :param json_object: select data key before pass
    :return:
    """
    add_object = Add()

    add_object.totalArea = json_object['offersSerialized']['totalArea']
    add_object.fullUrl = json_object['offersSerialized']['fullUrl']
    add_object.title = json_object['offersSerialized']['title']
    add_object.roomsCount = json_object['offersSerialized']['roomsCount']
    add_object.price = json_object['offersSerialized']['bargainTerms']['price']
    add_object.paymentPeriod = json_object['offersSerialized']['bargainTerms']['paymentPeriod']
    add_object.leaseTermType = json_object['offersSerialized']['bargainTerms']['leaseTermType']















