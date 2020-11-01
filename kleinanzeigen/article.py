
class Article:
    def __init__(self, name: str, price: int, negotiable: bool, url: str, date: str, image: str):
        self.name = name
        self.price = price
        self.negotiable = negotiable
        self.url = 'https://www.ebay-kleinanzeigen.de' + url
        self.date = date
        self.image = image

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