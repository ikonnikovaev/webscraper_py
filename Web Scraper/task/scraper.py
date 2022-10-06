from bs4 import BeautifulSoup
import os
import requests
import string

ARTICLES_URL = url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
ARTICLE_ROOT = 'https://nature.com'

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

def load_article(dir_name, title, url):
    full_url = f"{ARTICLE_ROOT}{url}"
    response = requests.get(full_url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find("div", {"class": "c-article-body"}).text.strip().encode()
        file_name = create_file_name(title)
        print(dir_name)
        print(file_name)
        file_path = os.path.join(dir_name, file_name)
        print(file_path)
        save_to_file(file_path, body)
    else:
        print(f'Error code {response.status_code}')



def load_articles(url, n_pages, type):
    for k in range(1, n_pages + 1):
        response = requests.get(url, params={'page': k})
        if not response:
            print(f'The URL returned {response.status_code}!')
        else:
            dir_name = f'Page_{k}'
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.findAll('article')
            for article in articles:
                if article.find('span', {'data-test': 'article.type'}).text.strip().lower() == type.strip().lower():
                    article_url = article.find('a', {'data-track-action': 'view article'}).get('href').strip()
                    article_title = article.find('a', {'data-track-action': 'view article'}).text.strip()
                    load_article(dir_name, article_title, article_url)
    print('Articles are saved!')



n_pages = int(input())
type = input()
load_articles(ARTICLES_URL, n_pages, type)
