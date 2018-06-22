# coding: utf-8
# import json
import os
import csv
import time
import requests
from bs4 import BeautifulSoup

path = os.getcwd()


def get_book_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    div = soup.find("div", {"class": "head-intro"})
    title = div.find("span", {"itemprop": "name"}).text.encode('utf-8')
    author = div.find("a").text.encode('utf-8')
    div = soup.find("ul", {"class": "details clearfix"}).contents[2]
    editor = div.find("span", {"class": "value"}).text.encode('utf-8')
    link = soup.find("img", {"title": title}).get('src').encode('utf-8')
    reviews = soup.find_all('p', {"itemprop": "description"})
    list_reviews = []
    for review in reviews:
        list_reviews.append(review.text.encode('utf-8'))
    if list_reviews:
        list_reviews.pop(0)
    rating = soup.find("span", {"itemprop": "ratingValue"})
    if rating:
        rating = rating.text
    writer.writerow([title, author, editor, link, rating, list_reviews])
    print title, author, link, editor, list_reviews, rating


def search_among_books(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    divs = soup.find("div", {"class": "product-result"})
    for div in divs:
        div = div.find("div", {"class": "description"})
        if div:
            url = div.find("a").get('href')
            get_book_data(url)
            print("I'm sleeping...Zzz")
            time.sleep(5)


if __name__ == '__main__':
    with open('dataset.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['title', 'author', 'editor',
                         'image_link', 'rating', 'reviews'])
        for i in range(1, 30):
            search_among_books(
                ("https://www.lafeltrinelli.it/libri/c-1/0/{}/?prkw=&prm=").
                format(i))
            print("I'm sleeping...Zzz")
            time.sleep(10)
