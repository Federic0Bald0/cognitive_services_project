import csv
import ast
from google.cloud import datastore
from difflib import SequenceMatcher
from google_api import call_vision_api

client = datastore.Client.from_service_account_json(
    'credentials_datastore.json')

CSV = 'dataset/dataset.csv'


# add starting dataset in dataset/dataset.csv
def add_csv():
    with open(CSV) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader, None)
        for row in reader:
            reviews = ast.literal_eval(row[6])
            add_book(row[0], row[1], row[3], row[4],
                     row[5], reviews, row[2])


# add a single book
def add_book(title, author, image, rating=None, price=None,
             reviews=None, editor=None):

    key = client.key('Book')
    book = datastore.Entity(
        key, exclude_from_indexes=['description'])

    book.update({
        'title': title,
        'author': author,
        'image': image,
        'editor': editor,
        'rating': rating,
        'price': price
    })
    client.put(book)

    for review in reviews:
        # only reviews with less then 1500 char are allowed
        if len(review) < 1500:
            add_review(book.key, review)

    return book.key


# add a review related to a book
def add_review(book_key, review):

    key = client.key('Review')
    rev = datastore.Entity(
        key, exclude_from_indexes=['description'])

    rev.update({
        'book_key': book_key,
        'review': review
    })

    client.put(rev)
    return rev.key


def delete_book(book_key):
    client.delete(book_key)


def list_books():
    query = client.query(kind='Book')
    query.projection = ['title']
    return list(query.fetch())


# next_cursor: "pointer" to the first not downloaded entry
# n: how many entries will be downloaded in one step
def get_some_books(cursor=None, limit=None):

    query = client.query(kind='Book')
    query_iter = query.fetch(start_cursor=cursor, limit=limit)
    page = next(query_iter.pages)

    books = list(page)
    next_cursor = query_iter.next_page_token

    return books, next_cursor


def get_reviews(book_id):

    query = client.query(kind='Review')
    query.add_filter('book_key', '=', book_id)
    results = list(query.fetch())

    return results


def search_book(generic_title, cursor=None, similarity=[0, 0], best_book=None):

    books, next_cursor = get_some_books(cursor=cursor)
    similarity = similarity
    best_book = best_book

    for book in books:
        if book:
            to_be_matched = [book.get('title'), book.get('author')]
            # print to_be_matched

            best_ratios = match_blocks(to_be_matched, generic_title)
            # print best_ratios

            if is_better(best_ratios, similarity):
                similarity = best_ratios
                best_book = book

    if next_cursor:
        return search_book(generic_title, next_cursor, similarity, best_book)

    return (similarity, best_book)


# check if the ratio1 is better than ratio2
def is_better(ratio1, ratio2):
    diff_title = ratio1[0] - ratio2[0]
    diff_author = ratio1[1] - ratio2[1]

    if diff_title + diff_author >= 0:
        return True
    else:
        return False


# ratio_index = 0: analyzing title
# ratio_index = 1: analyzing author
def match_blocks(source, detected):
    """
    source : text coming from datastore
    detected : text coming from vision API
    """
    best_ratios = [0, 0]
    ratio_index = 0

    for source_text in source:
        for det_text in detected:
            # check similaruty between every possible combination
            # of string coming from source and detected
            ratio = get_strings_diff(det_text, source_text)
            if ratio > best_ratios[ratio_index]:
                best_ratios[ratio_index] = ratio
        # this is just because we assume that source hasn't
        # length grater than 2.
        # should be considered also editor : TODO
        ratio_index = 1

    return best_ratios


def get_strings_diff(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()


def find_book(book_file):

    blocks = call_vision_api(book_file)
    return blocks, search_book(blocks)
