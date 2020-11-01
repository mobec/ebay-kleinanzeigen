from datetime import datetime

class Article:
    def __init__(self, ebay_kleinanzeigen_id: int, name: str, price: str, negotiable: bool, url: str, date: datetime):
        self.ebay_kleinanzeigen_id = ebay_kleinanzeigen_id
        self.name = name
        self.price = price
        self.negotiable = negotiable
        self.url = 'https://www.ebay-kleinanzeigen.de' + url
        self.date = date
        self.image = None

    def __repr__(self):
        return f'{self.name} - {self.price} - {self.date}'

    def __str__(self):
        result = f'{self.name} - {self.price}'
        if self.negotiable:
            result += ' VB'
        result += f'\n\t{self.date}\n'

        result += self.url
        result += '\n'
        return result