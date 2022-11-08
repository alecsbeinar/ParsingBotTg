import json
import re

import requests
from bs4 import BeautifulSoup

# для преобразования в Unixtimestamp (количетсво секунд с 1 января 1970)
from datetime import datetime
import time


def get_first_news():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    url = 'https://ont.by/news/categories/accidents'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    article_cards = soup.find_all("a", class_="b-news-preview") # забираем все элементы с тегом а и классом

    news_dict = {}

    for article in article_cards:
        article_title = article.find("h3", class_="b-news-preview__title").text.strip()
        article_url = f"https://ont.by{article.get('href')}"

        # перевод
        article_data_time = article.find("time").get('datetime')
        date_from_iso = datetime.fromisoformat(article_data_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
        article_data_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

        # айдишник - последние три слова в адресе сайта
        article_id = article_url.split("-")[-3:]
        article_id = ''.join(article_id)

        # заносим все данные
        news_dict[article_id] = {
            'article_date_timestamp': article_data_timestamp,
            'article_title': article_title,
            'article_url': article_url
        }

        # сохраняем все в файл
        with open("news_dict.json", "w") as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    # берем все данные из существующего файла
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    url = 'https://ont.by/news/categories/accidents'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    article_cards = soup.find_all("a", class_="b-news-preview")  # получаем все статьи на данный момент

    fresh_news = {}  # новости, которых нет в старом файле
    for article in article_cards:
        article_url = f"https://ont.by{article.get('href')}"
        article_id = article_url.split("-")[-3:]
        article_id = ''.join(article_id)

        if article_id in news_dict:
            continue  # если есть, то пропуск
        else:
            article_title = article.find("h3", class_="b-news-preview__title").text.strip()

            article_data_time = article.find("time").get('datetime')
            date_from_iso = datetime.fromisoformat(article_data_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            article_data_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

            # заносим в старый файл
            news_dict[article_id] = {
                'article_date_timestamp': article_data_timestamp,
                'article_title': article_title,
                'article_url': article_url
            }

            # параллельно заносим в новый
            fresh_news[article_id] = {
                'article_date_timestamp': article_data_timestamp,
                'article_title': article_title,
                'article_url': article_url
            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def get_news_keyword(keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    url = 'https://ont.by/news/categories/accidents'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    news = soup.find_all("span", text=re.compile(keyword))
    d = {}
    for n in news:
        d[n.text.strip()] = 'https://ont.by' + n.find_parent("div", class_="news-category__cell").find("a").get("href")
    return d

def main():
    # для запуска впервые
    # get_first_news()

    # print(check_news_update())
    get_news_keyword('ДТП')


if __name__ == '__main__':
    main()
