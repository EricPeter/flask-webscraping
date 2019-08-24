import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy

url = 'https://www.riverisland.com/c/men/seasonal-offers?icid=mhp/winter-treats/m/seasonal-offers/cat'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

name_box = soup.find_all('div', attrs={'class':'product__title ui-body-text'})
price_box = soup.find_all('div', attrs={'class':'product-price__headline product-price__headline--sale'})

for product in zip(name_box,price_box):
    name,price=product
    name_proper=name.text.strip()
    price_proper=price.text.strip()
    print(name_proper,'-',price_proper)