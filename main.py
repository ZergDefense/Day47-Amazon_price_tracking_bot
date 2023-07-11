import os

from bs4 import BeautifulSoup
import requests
import smtplib
import unicodedata

URL = "https://mstore.hu/xiaomi-smart-air-purifier-4-lite-okos-legtisztito-bhr5274gl-2507?keyword=Purifier"
TARGET_PRICE = 60000

my_email = os.environ['MY_EMAIL']
password = os.environ['PASSWORD']


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


response = requests.get(url=URL)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

product_name = strip_accents(soup.find(name="span", class_="product-page-product-name").getText())
print(product_name)

price = float(soup.find(name="span", class_="product-price-special").getText().split()[0].replace(".", ""))

print(price)

if price <= TARGET_PRICE:
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="szabo.gergo.bme@gmail.com",
            msg=f"Subject:Price alert!\n\n{product_name} is now {int(price)}HUF\n\n{URL}")
