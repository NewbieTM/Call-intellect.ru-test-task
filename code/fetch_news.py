import requests
from bs4 import BeautifulSoup

def fetch_latest_news(keywords):
    url = f"https://www.babyblog.ru/search?request={'+'.join(keywords)}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='post-body-content-info')
    news = []
    for article in articles:
        summary = article.find('p').text
        link = article.find('a')['href']
        news.append({'summary': summary, 'link': f'https://www.babyblog.ru{link}'})
    return news
