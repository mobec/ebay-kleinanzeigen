from datetime import datetime

class Article:
    def __init__(self, ebay_kleinanzeigen_id: int, name: str, price: str, url: str, date: datetime):
        self.ebay_kleinanzeigen_id = ebay_kleinanzeigen_id
        self.name = name
        self.price = price
        self.url = 'https://www.ebay-kleinanzeigen.de' + url
        self.date = date
        self.image = None

    def __repr__(self):
        return f'{self.name} - {self.price} - {self.date}'

    def __str__(self):
        result = f'{self.name} - {self.price}'
        result += f'\n\t{self.date}\n'

        result += self.url
        result += '\n'
        return result