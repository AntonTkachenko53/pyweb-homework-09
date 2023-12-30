from bs4 import BeautifulSoup
import json
import requests


base_url = 'https://quotes.toscrape.com'


def count_pages():
    url_to_count_pages = 'https://quotes.toscrape.com/page/{}'
    current_page = 1
    while True:
        response = requests.get(url_to_count_pages.format(current_page))
        soup = BeautifulSoup(response.text, 'html.parser')
        li_next = soup.select_one('div[class=col-md-8] nav ul[class=pager] li[class=next]')
        if li_next is not None:
            current_page += 1
        else:
            break
    return current_page


def get_urls():
    return [base_url + f'/page/{i}' for i in range(1, count_pages() + 1)]


def get_quotes():
    data = []
    for url in get_urls():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class=col-md-8] div[class=quote]')
        for elem in content:
            result = {}
            tags = elem.select('div[class=tags] a[class=tag]')
            result['tags'] = [tag.text for tag in tags]
            author = elem.select_one('span small[class=author]').text
            result['author'] = author
            quote = elem.select_one('span[class=text]').text
            result['quote'] = quote
            data.append(result)
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_authors():
    data_to_json = []
    authors = set()
    for url in get_urls():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class=col-md-8] div[class=quote]')
        for elem in content:
            author = elem.find_all('span')[1].find('a')['href']
            authors.add(author)

    authors_urls = [base_url + f"{author}" for author in authors]

    for url in authors_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class=author-details]')
        for elem in content:
            result = {}
            fullname = elem.find('h3').text
            result['fullname'] = fullname
            born_date = elem.select_one('p span[class=author-born-date]').text
            result['born_date'] = born_date
            born_location = elem.select_one('p span[class=author-born-location]').text
            result['born_location'] = born_location
            description = elem.find('div', attrs={'class': 'author-description'}).text
            result['description'] = description.strip()
            data_to_json.append(result)
    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_json, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    get_quotes()
    get_authors()
