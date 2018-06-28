# coding: utf-8
# import json
import os
import csv
import time
import requests
from bs4 import BeautifulSoup

path = os.getcwd()


# get data from book page
def get_book_data(url):
    r = requests.get(url)
    # preparing soup for parsing
    soup = BeautifulSoup(r.content, 'html.parser')
    # div title, author
    div = soup.find("div", {"class": "head-intro"})
    title = div.find("span", {"itemprop": "name"}).text.encode('utf-8')
    author = div.find("a").text.encode('utf-8')
    # div editor
    div = soup.find("ul", {"class": "details clearfix"}).contents[2]
    editor = div.find("span", {"class": "value"}).text.encode('utf-8')
    # parsing other useful info
    link = soup.find("img", {"title": title}).get('src').encode('utf-8')
    price = soup.find("meta", {"itemprop": "price"})
    if price:
        price = price.get('content')
    reviews = soup.find_all('p', {"itemprop": "description"})
    list_reviews = []
    # creating list reviews for db
    for review in reviews[:1]:
        list_reviews.append(review.text.encode('utf-8'))
    rating = soup.find("span", {"itemprop": "ratingValue"})
    if rating:
        rating = rating.text
    writer.writerow([title, author, editor, link, rating, price, list_reviews])
    print title, author, link, editor, rating, price, list_reviews


# get data from page with list of book
def search_among_books(url):
    r = requests.get(url)
    # preparing soup for parsing
    soup = BeautifulSoup(r.content, 'html.parser')
    # div containing list of the books in the page
    divs = soup.find("div", {"class": "product-result"})
    for div in divs:
        div = div.find("div", {"class": "description"})
        if div:
            url = div.find("a").get('href')
            get_book_data(url)
            # time overhead to avoid overloading requests
            print("I'm sleeping...Zzz")
            time.sleep(5)


if __name__ == '__main__':
    with open('dataset.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['title', 'author', 'editor',
                         'image_link', 'rating', 'price', 'reviews'])
        # scrape content from 30 pages with list of books.
        for i in range(1, 31):
            search_among_books(
                ("https://www.lafeltrinelli.it/libri/c-1/0/{}/?prkw=&prm=").
                format(i))
            # time overhead to avoid overloading requests
            print("I'm sleeping...Zzz")
            time.sleep(10)
