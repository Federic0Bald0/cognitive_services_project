# coding: utf-8
import os
from werkzeug import secure_filename
from src.datastore import find_book, add_book
from src.areSimilar import sift_match_images, bf
from flask import Flask, redirect, url_for, request, render_template, flash
from skimage import io

app = Flask(__name__)
app.secret_key = 'vogliamo30elode'
app.config['UPLOAD_FOLDER'] = 'static/pictures'


# Templates and File Uploading ###


@app.route('/')
def show_home():
    return render_template('home.html')


@app.route('/result', methods=['POST'])
def show_result():
    if request.method == 'POST':
        f = request.files['pic']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        book_details = find_book(filename)
        # temporary threshold for match
        if book_details[1][0][0] < 0.5 or book_details[1][0][1] < 0.5:
            flash('The book is not available in our database, \
                   would you like to enrich our application adding \
                   this book ?')
            return render_template('insert.html', picture=filename)
        return render_template(
            'result.html',
            picture=filename,
            blocks=book_details[0],
            result=('Title: ' +
                    book_details[1][1].get('title').encode('utf-8') +
                    ', Author: ' +
                    book_details[1][1].get('author').encode('utf-8')),
            similarities=book_details[1][0],
            dataset_image_link=book_details[1][1].get('image'),
            local=book_details[1][1].get('local')
            )


@app.route('/matches', methods=['POST', 'GET'])
def show_matches():
    # According to which tecnique is selected, good percentage
    # and matches image are shown
    if request.form['tecnique'] == 'sift':
        # if the image is stored locally
        if request.args.get('local'):
            query = io.imread(request.args.get('query').encode('utf-8'))
        else:
            # Convert links into numpy array (right format for opencv)
            query = io.imread('https:' + request.args.get('query')
                              .encode('utf-8'))
        image = io.imread(os.path.join(app.config['UPLOAD_FOLDER'],
                                       request.args.get('image')
                                       .encode('utf-8')))
        good_perc = sift_match_images(bf, query, image)
        return render_template('matches.html',
                               matches_image='static/matches.png',
                               good=good_perc)


@app.route('/insert', methods=['POST', 'GET'])
def add_new_book():
    # add new book to database
    if request.method == 'POST':

        title = request.form['title']
        if not title:
            flash('You must insert a Title')
            return render_template('insert.html')
        else:
            title = title.lower()
        author = request.form['author']
        if not author:
            flash('You must insert a Author')
            return render_template('insert.html')
        else:
            author = author.lower()
        editor = request.form['editor']
        if editor:
            editor = editor.lower()
        rating = request.form['rating']
        if rating:
            rating = int(rating)
            if rating < 1 or rating > 5:
                flash('Rating must be number between 1 and 5')
                return render_template('insert.html')
        price = request.form['price']
        review = request.form['review']
        if len(review) > 1500:
            flash('You exceeded the limit of 1500 characters in the review')
            return render_template('insert.html')
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

'''
# Hello World #

@app.route('/')
def helloWorld():
    return 'Hello World!'


@app.route('/hello/<name>')
def hello_world(name):
    return 'Hello %s!' % name


@app.route('/admin')
def hello_admin():
    return 'Hello Adimn'


@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello, guest %s!' % guest


@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))

################################

# POST Request to Python from HTML ###


@app.route('/success/<name>')
def success(name):
    return "Welcome %s!" % name


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

##########################################
'''
