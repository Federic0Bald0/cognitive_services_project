import csv
from google.cloud import datastore
from difflib import SequenceMatcher

client = datastore.Client.from_service_account_json(
                        'credentials_datastore.json')

CSV = 'datastore/dataset_test.csv'


def add_csv():
    with open(CSV) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader, None)
        for (i, row) in enumerate(reader):
            # i+1 because id must not be 0
            add_book(i+1, row[0], row[1], row[3],
                     editor=row[2], reviews=row[4])


def add_book(book_id, title, author, image, editor=None,
             reviews=None, descriptions=None):

    key = client.key('Book', book_id)
    book = datastore.Entity(
        key, exclude_from_indexes=['description'])
    print book

    book.update({
        'title': title,
        'author': author,
        'image': image,
        'editor': editor,
        'descriptions': descriptions
    })

    client.put(book)
    return book.key


def delete_book(book_key):
    client.delete(book_key)


def list_books():
    query = client.query(kind='Book')
    query.projection = ['title']
    return list(query.fetch())


# next_cursor: "pointer" to the first not downloaded entry
# n: how many entries will be downloaded in one step
def get_some_books(cursor=None):
    n = 10
    query = client.query(kind='Book')
    query_iter = query.fetch(start_cursor=cursor, limit=n)
    page = next(query_iter.pages)

    books = list(page)
    next_cursor = query_iter.next_page_token

    return books, next_cursor


def search_book(generic_title):

    books, next_cursor = get_some_books()
    similarity = 0
    most_likely = 0

    for book in books:
        if book:
            to_be_matched = book.get('title') + book.get('author')
            print to_be_matched
            ratio = get_strings_diff(to_be_matched, generic_title)
            if ratio > similarity:
                similarity = ratio
                key = book.key

    return similarity, key


def get_strings_diff(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()

if __name__ == '__main__':
    # add_csv()
    # print list_books()
    print(search_book("Io, te e il ,Marzia Sici"))



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