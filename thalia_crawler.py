import requests
from bs4 import BeautifulSoup


class Product:
    def __init__(self, title, author, link, price):
        self.title = title
        self.author = author
        self.link = link
        self.price = price


def get_results(search):
    products = []

    r = requests.get('https://www.thalia.de/suche?utf8=%E2%9C%93&filterPATHROOT=&sq=' + search)
    doc = BeautifulSoup(r.text, 'html.parser')
    for product in doc.select('.row.product'):
        title = product.select_one('.oProductTitle').text
        try:
            author = product.select_one('.oAuthor').text
        except AttributeError:
            continue
        link = 'https://www.thalia.de' + product.select_one('a').attrs['href']
        price_list = product.select_one('.oPrice').text.split(',')
        price_list[1] = price_list[1][:-2]
        price = price_list[0] + '.' + price_list[1]
        products.append(Product(title, author, link, price))

    return products