import requests
import datetime as dt
from datetime import timedelta
import smtplib

MY_EMAIL = "**email**"
MY_PASSWORD = "**password**"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters_for_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "**key**"
}
response = requests.get(STOCK_ENDPOINT, params=parameters_for_stock)
data = response.json()

today = dt.datetime.today().date()

yesterday = today + timedelta(days=-1)

yesterday_closing_stock_price = float(data["Time Series (Daily)"][f"{yesterday}"]["4. close"])

day_before_yesterday = today + timedelta(days=-2)

day_before_yesterday_closing_stock_price = float(data["Time Series (Daily)"][f"{day_before_yesterday}"]["4. close"])

difference = round(yesterday_closing_stock_price - day_before_yesterday_closing_stock_price)

percentage_difference = round((difference / day_before_yesterday_closing_stock_price) * 100)

parameters_for_news = {
    "q": "tesla",
    "from": yesterday,
    "sortBy": "publishedAt",
    "apiKey": "**key**"
}

if percentage_difference > 2:
    # print("Get News")

    response_n = requests.get(NEWS_ENDPOINT, params=parameters_for_news)
    data_n = response_n.json()
    titles = data_n["articles"][0:3]

    list_of_news = []

    for news in titles:
        list_of_news.append(news["title"])


    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()

        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:TSLA: 🔺{percentage_difference}%\n\n{list_of_news[0]}\n{list_of_news[1]}\n{list_of_news[2]}".encode('utf-8')
        )

if percentage_difference < - 2:

    response_n = requests.get(NEWS_ENDPOINT, params=parameters_for_news)
    data_n = response_n.json()
    titles = data_n["articles"][0:3]

    list_of_news = []

    for news in titles:
        list_of_news.append(news["title"])

    # print(list_of_news)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()

        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:TSLA: 🔻{percentage_difference * - 1}%\n\n{list_of_news[0]}\n{list_of_news[1]}\n{list_of_news[2]}".encode('utf-8')
        )
