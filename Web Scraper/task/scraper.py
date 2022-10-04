import requests
from bs4 import BeautifulSoup

def get_quote(url):
    error_message = "Invalid quote resource!"
    response = requests.get(url)
    if not response:
        return error_message
    quote = response.json().get('content')
    if quote:
        return quote
    return error_message

def get_movie_info(url):
    error_message = "Invalid movie page!"
    response = requests.get(url)
    if not response:
        return error_message
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1')
    description = soup.find('span', {'data-testid': 'plot-l'})
    if title is None or description is None:
        return error_message
    return {'title': title.text, 'description': description.text}


print('Input the URL:')
url = input()
print(get_movie_info(url))
