from google.cloud import datastore

client = datastore.Client.from_service_account_json(
                        'cognitive_local/credentials.json')


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
    return list(query.fetch())


book_key = add_book(1,
                    title="Harry Potter e la pietra filosofale",
                    author="J. K. Rowling",
                    image="this is a placeholder",
                    )
print(list_books())
# delete_book(book_key)