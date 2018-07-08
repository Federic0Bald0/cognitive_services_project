# coding: utf-8
import os
from werkzeug import secure_filename
from src.areSimilar import sift_match_images, flann
from src.datastore import find_book, add_book, get_reviews, add_review, client
from flask import Flask, redirect, url_for, request, render_template, flash

app = Flask(__name__)
app.secret_key = 'vogliamo30elode'
app.config['UPLOAD_FOLDER'] = 'static/pictures'

# Templates and File Uploading


@app.route('/')
def show_home():
    return render_template('home.html')


@app.route('/result', methods=['POST'])
def show_result():
    if request.method == 'POST':

        f = request.files['pic']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # book retrieved from datastore
        # BLOCK SEARCH
        book_details = find_book(filename)
        book = book_details[1][1]
        good_perc = sift_match_images(flann,
                                      book.get('image'),
                                      filename,
                                      book.get('local'))
        # LINE SEARCH
        book_details_lines = find_book(filename)
        book_lines = book_details_lines[1][1]
        good_perc_lines = sift_match_images(flann,
                                            book_lines.get('image'),
                                            filename,
                                            book_lines.get('local'))

        # temporary threshold for match
        if (book_details[1][0][0] > 0.5 and
                book_details[1][0][1] > 0.5 and
                good_perc/100 > 0.4):

            if ((book_details_lines[1][0][0] - book_details[1][0][0]) +
                    (book_details_lines[1][0][1] - book_details[1][0][1]) +
                    (good_perc_lines - good_perc) > 0):
                # if similarities founded by lines are better,
                # consider them instead of blocks
                book_details = book_details_lines
                book = book_lines

        else:
            # there is no match for the inserted book
            flash('The book is not available in our database, \
                       would you like to enrich our application adding \
                       this book ?')
            return render_template('insert.html', picture=filename)

        id = book.key.id
        key = client.key('Book', id)
        # get review for the retrieved book
        reviews = get_reviews(key)
        reviews = [review.get('review').decode('utf-8')
                   for review in reviews]
        return render_template(
            'result.html',
            picture=filename,
            blocks=book_details[0],
            book_id=id,
            price=book.get('price'),
            rating=book.get('rating'),
            result=('Title: ' +
                    book.get('title').encode('utf-8') +
                    ', Author: ' +
                    book.get('author').encode('utf-8')),
            similarities=book_details[1][0],
            dataset_image_link=book.get('image'),
            local=book.get('local'),
            reviews=reviews
        )


@app.route('/comment', methods=['POST'])
# add comment to book
def store_comment():
    review = request.form['review']
    if len(review) > 1500:
        flash('Your comment is too long')
        render_template('home.html')
    if len(review) == 0:
        flash("You didn't type anything")
        render_template('home.html')
    book_id = request.args.get('book_id')
    book_key = client.key('Book', long(book_id))
    add_review(book_key, review.encode('utf-8'))
    flash('Thank you, your comment is really valuable\
          for us')
    return render_template('home.html')


@app.route('/matches', methods=['POST', 'GET'])
# show sift matches
def show_matches():
    # According to which tecnique is selected, good percentage
    # and matches image are shown
    # if request.form['tecnique'] == 'sift': TODO
    # if the image is stored locally
    good_perc = sift_match_images(flann,
                                  request.args.get('query'),
                                  request.args.get('image'),
                                  request.args.get('local'))

    return render_template('matches.html',
                           matches_image='static/matches.png',
                           good=good_perc)


@app.route('/insert', methods=['POST', 'GET'])
def add_new_book():
    # add new book to database
    if request.method == 'POST':
        # title
        title = request.form['title']
        if not title:
            flash('You must insert a Title')
            return render_template('insert.html')
        else:
            title = title.lower()
        # author
        author = request.form['author']
        if not author:
            flash('You must insert a Author')
            return render_template('insert.html')
        else:
            author = author.lower()
        # editor
        editor = request.form['editor']
        if editor:
            editor = editor.lower()
        # rating
        rating = request.form['rating']
        if rating:
            rating = int(rating)
            if rating < 1 or rating > 5:
                flash('Rating must be number between 1 and 5')
                return render_template('insert.html')
        # price
        price = request.form['price']
        # comment
        review = request.form['review']
        if len(review) > 1500:
            flash('You exceeded the limit of 1500 characters in the review')
            return render_template('insert.html')
        # picture of the book stored locally
        picture = request.args.get('picture')
        image = os.path.join(app.config['UPLOAD_FOLDER'], picture)
        key = add_book(title, author, image, rating,
                       price, [review], editor, local=True)
        if key:
            flash('New book succesfully inserted')
            print key
            return render_template('home.html')
        flash('Error inserting book')
        return render_template('home.html')


# Added to avoid caching of the match image
# Ugly, but seems to work
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
