import requests
from bs4 import BeautifulSoup
import string

ARTICLES_URL = "https://nature.com/nature/articles?sort=PubDate&year=2020&page=3"
ARTICLE_ROOT = "https://nature.com"

def get_quote(url):
    error_message = 'Invalid quote resource!'
    response = requests.get(url)
    if not response:
        return error_message
    quote = response.json().get('content')
    if quote:
        return quote
    return error_message

def get_movie_info(url):
    error_message = 'Invalid movie page!'
    response = requests.get(url)
    if not response:
        return error_message
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1')
    description = soup.find('span', {'data-testid': 'plot-l'})
    if title is None or description is None:
        return error_message
    return {'title': title.text, 'description': description.text}

def load_html(url, file='source.html'):
    response = requests.get(url)
    if not response:
        print(f'The URL returned {response.status_code}!')
    else:
        with open(file, 'wb') as f:
            f.write(response.content)
            print('Content saved.')
            f.close()

def create_file_name(title):
    file_name = ""
    for ch in title:
        if ch in string.punctuation:
            pass
        elif ch in string.whitespace:
            file_name += '_'
        else:
            file_name += ch
    return file_name + '.txt'

def save_to_file(file_name, body):
    with open(file_name, 'wb') as f:
        f.write(body)
        f.close()


def load_article(title, url):
    full_url = f"{ARTICLE_ROOT}{url}"
    response = requests.get(full_url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find("div", {"class": "c-article-body"}).text.strip().encode()
        file_name = create_file_name(title)
        save_to_file(file_name, body)
    else:
        print(f'Error code {response.status_code}')
def load_all_articles(url):
    response = requests.get(url)
    if not response:
        print(f'The URL returned {response.status_code}!')
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.findAll('article')
        for article in articles:
            if article.find('span', {'data-test': 'article.type'}).text.strip().lower() == 'news':
                article_url = article.find('a', {'data-track-action': 'view article'}).get('href').strip()
                article_title = article.find('a', {'data-track-action': 'view article'}).text.strip()
                load_article(article_title, article_url)
        print('Articles are saved!')


# print('Input the URL:')
# url = input()
# print(get_movie_info(url))
url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3'
load_all_articles(url)
