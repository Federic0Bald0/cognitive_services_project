import csv
import ast
from google.cloud import datastore
from difflib import SequenceMatcher

client = datastore.Client.from_service_account_json(
                        'credentials_datastore.json')

CSV = 'dataset/dataset.csv'


def add_csv():
    with open(CSV) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader, None)
        for (i, row) in enumerate(reader):
            # i+1 because id must not be 0
            reviews = ast.literal_eval(row[6])
            add_book(i+1, row[0], row[1], row[3], row[4],
                     row[5], reviews, row[2])


def add_book(book_id, title, author, image, rating, price,
             reviews, editor, descriptions=None):

    key = client.key('Book', book_id)
    book = datastore.Entity(
        key, exclude_from_indexes=['description'])
    # print book

    book.update({
        'title': title,
        'author': author,
        'image': image,
        'editor': editor,
        'rating': rating,
        'price': price,
        'descriptions': descriptions
    })
    for review in reviews:
        # only reviews with less then 1500 char are allowed
        if len(review) < 1500:
            add_review(key, review)

    client.put(book)
    return book.key


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
def get_some_books(cursor=None):
    # n = 10
    query = client.query(kind='Book')
    query_iter = query.fetch(start_cursor=cursor)
    page = next(query_iter.pages)

    books = list(page)
    next_cursor = query_iter.next_page_token

    return books, next_cursor


def search_book(generic_title, cursor=None, similarity=0, key=None):

    books, next_cursor = get_some_books(cursor=cursor)
    similarity = similarity
    key = key

    for book in books:
        if book:
            to_be_matched = book.get('title') + book.get('author')
            print to_be_matched
            ratio = get_strings_diff(to_be_matched, generic_title)
            if ratio > similarity:
                similarity = ratio
                key = book.key

    if next_cursor:
        return search_book(generic_title, next_cursor, similarity, key)

    return similarity, key


def get_strings_diff(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()

if __name__ == '__main__':
    # add_csv()
    # print list_books()
    # get_some_books()
    print(search_book("Madagascar. Con mappa,Heiko Hooge,Dumont"))


# book_key = add_book(3,
#                     title="Harry Potter e i doni della morte",
#                     author="J. K. Rowling",
#                     image="this is a placeholder",
#                     )

# books, next_cursor = get_some_books()
# print books
# books, _ = get_some_books(next_cursor)
# print books

# delete_book(book_key)
