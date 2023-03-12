import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
import os

URL = "https://www.amazon.com/Hollow-Knight-Vinyl-Design-Occasion/dp/B07T3Y5CKH/ref=sr_1_2?crid=C0P5M3BXISEB&keywords=hollow+knight&qid=1678650414&sprefix=hollow+kni%2Caps%2C227&sr=8-2"
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.9"
}

response = requests.get(url=URL, headers=headers)
# print(response.text)
soup = BeautifulSoup(response.text, parser="lxml", features="lxml")
# print(soup.prettify())

price = soup.find(name="span", class_="a-price a-text-price a-size-medium apexPriceToPay").getText()
price_without_currency = price.split("$")[1].strip("$")
price_as_float = float(price_without_currency)
print(price_as_float)

if price_as_float < 30:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=f"Subject:Amazon Price Alert!\n\nHollow Knight Vinyl "
                                                                 f"Wall Clock, Hollow Knight Design Gift for Any Occasion "
                                                                 f"Art is now ${price_as_float}\n{URL}")

