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
            add_book(i + 1, row[0], row[1], row[3], row[4],
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


def search_book(generic_title, cursor=None, similarity=[0, 0], key=None):

    books, next_cursor = get_some_books(cursor=cursor)
    similarity = similarity
    key = key

    for book in books:
        if book:
            to_be_matched = [book.get('title'), book.get('author')]
            print to_be_matched

            best_ratios = match_blocks(to_be_matched, generic_title)
            print best_ratios

            if is_better(best_ratios, similarity):
                similarity = best_ratios
                key = book.key

    if next_cursor:
        return search_book(generic_title, next_cursor, similarity, key)

    # query = client.query(kind='Book')
    # first_key = client.key(u'Book', '1006L')
    # print first_key
    # print 'query: ', query.key_filter(first_key, '>')
    return similarity, client.get(key)


# check if the ratio1 is better than ratio2
def is_better(ratio1, ratio2):
    diff_title = ratio1[0] - ratio2[0]
    diff_author = ratio1[1] - ratio2[1]

    if diff_title + diff_author > 0:
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


if __name__ == '__main__':
    # add_csv()
    # print list_books()
    # get_some_books()
    print(search_book(["the police. many miles away,giovanni pollastri,sagoma",
                       "the police", "giovanni pollastri"]))


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
