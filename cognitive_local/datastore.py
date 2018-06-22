from google.cloud import datastore

client = datastore.Client.from_service_account_json(
                        './credentials.json')


def add_book(book_id, title, author, image, editor=None):

    key = client.key('Book', book_id)
    book = datastore.Entity(
        key, exclude_from_indexes=['description'])
    print book

    book.update({
        'title': title,
        'author': author,
        'image': image,
        'editor': editor
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
    n = 1
    query = client.query(kind='Book')
    query_iter = query.fetch(start_cursor=cursor, limit=n)
    page = next(query_iter.pages)

    books = list(page)
    next_cursor = query_iter.next_page_token

    return books, next_cursor



book_key = add_book(3,
                    title="Harry Potter e i doni della morte",
                    author="J. K. Rowling",
                    image="this is a placeholder",
                    )
books, next_cursor = get_some_books()
print books
books, _ = get_some_books(next_cursor)
print books
# delete_book(book_key)