import requests
import time
from bs4 import BeautifulSoup

# Telegram Bot details
telegram_bot_token = '6380162674:AAGsjjHmchSWaIRCLvqinIBCMq41DjNLMl0'
telegram_channel_username = '@burh12345'

url = 'https://www.fanabc.com/%e1%88%b5%e1%8d%93%e1%88%ad%e1%89%b5'

response = requests.get(url)
content2 = response.content

def scrape_data(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    news = []
    items = soup.find_all('a', class_='img-cont b-loaded') #!
    for item in items:
        category = item.find('div', class_='term-badges floated').text if item.find('div', class_='term-badges floated') else "Category not found"
        date = item.find('div', class_='post-meta').text if item.find('div', class_='post-meta') else "Date not found"
        headline = item.find('h2', class_='title').text if item.find('h2', class_='title') else "Headline not found"
        news.append({
            "category": category,
            "date": date,
            "headline": headline
        })
    return news

def send_message_to_telegram(message):
    send_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        "chat_id": telegram_channel_username,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(send_message_url, data=data)
    if response.status_code != 200:
        print("Failed to send message to Telegram channel.")

news_data = scrape_data(content2)

for news in news_data:
    caption = f"<b>News Category:</b> {news['category']}\n"
    caption += f"<b>News Headlines:</b> {news['headline']}\n"
    caption += f"<b>News Date:</b> {news['date']}\n"
    send_message_to_telegram(caption)
    time.sleep(60)
