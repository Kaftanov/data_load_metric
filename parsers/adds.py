class ShortAdd:
    title = ''
    sub_title = ''
    subway_station = ''
    address = ''
    price = 0.0
    sub_items = []
    short_description = ''
    holder = ''
    source = ''
    url = ''

    def __init__(self, source):
        self.source = source

    def __str__(self):
        return 'Title: ' + self.title + '\n' \
               + 'Sub Title: ' + self.sub_title + '\n' \
               + 'Subway Station: ' + self.subway_station + '\n' \
               + 'Address: ' + self.address + '\n' \
               + 'Price: ' + str(self.price) + '\n' \
               + 'Sub_items: ' + str(self.sub_items) + '\n' \
               + 'Short description: ' + self.short_description + '\n' \
               + 'Holder: ' + self.holder + '\n' \
               + 'Direct Link: ' + self.url + '\n' \
               + '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

    def get_list_values(self):
        return [self.title, self.sub_title, self.subway_station, self.address, self.price,
                '|'.join(self.sub_items), self.short_description, self.holder, self.source, self.url]

    @staticmethod
    def get_str_attributes():
        return ['title', 'sub_title', 'subway_station', 'address', 'price', 'sub_items', 'short_description', 'holder',
                'source', 'url']
