import csv
import time
import matplotlib.pyplot as plt
from src.datastore import find_book
from src.areSimilar import sift_match_images, flann


test_CSV_positive = 'dataset/testset_positive.csv'
test_CSV_negative = 'dataset/testset_negative.csv'


def run_test(test_CSV):

    with open(test_CSV) as csvtest:
        reader = csv.reader(csvtest, delimiter=',')
        header = next(reader, None)
        book_number = []
        title_blocks = []
        author_blocks = []
        time_blocks = []
        match_blocks = []
        title_lines = []
        author_lines = []
        time_lines = []
        match_lines = []
        for i, row in enumerate(reader):
            book_number.append(i)
            filename = row[2]
            print '+++++++++++++++++++++'
            print filename
            print '+++++++++++++++++++++'
            # BLOCK SEARCH
            ti_blocks = int(round(time.time() * 1000))
            book_details_blocks = find_book(filename)
            tf_blocks = int(round(time.time() * 1000))
            tot_blocks_search = tf_blocks - ti_blocks
            book_blocks = book_details_blocks[1][1]
            good_perc_blocks = sift_match_images(flann,
                                                 book_blocks.get('image'),
                                                 filename)

            title_test = book_blocks.get('title')
            author_test = book_blocks.get('author')

            title_blocks.append(book_details_blocks[1][0][0] * 100)
            author_blocks.append(book_details_blocks[1][0][1] * 100)
            time_blocks.append(tot_blocks_search)
            match_blocks.append(good_perc_blocks)

            print '********************'
            print 'BLOCK SEARCH'
            print 'test case: ' + str(i + 1)
            print 'ratio title: ' + (str(book_details_blocks[1][0][0] *
                                     100) + '%')
            print 'ration author: ' + (str(book_details_blocks[1][0][1] *
                                       100) + '%')
            print 'precision image match: ' + str(good_perc_blocks) + '%'
            print 'time: ' + str(tot_blocks_search) + ' millisecond'
            if (book_details_blocks[1][0][0] > 0.5 and
                    book_details_blocks[1][0][1] > 0.5 and
                    good_perc_blocks/100 > 0.4):
                print 'GOOD blocks match'
            else:
                print 'BAD blocks match'
            if title_test != row[0] and author_test != row[1]:
                print title_test, author_test
            # LINE SEARCH
            ti_lines = int(round(time.time() * 1000))
            book_details_lines = find_book(filename)
            tf_lines = int(round(time.time() * 1000))
            tot_lines_search = tf_lines - ti_lines
            book_lines = book_details_lines[1][1]
            good_perc_lines = sift_match_images(flann,
                                                book_lines.get('image'),
                                                filename)

            title_test = book_lines.get('title')
            author_test = book_lines.get('author')

            title_lines.append(book_details_lines[1][0][0] * 100)
            author_lines.append(book_details_lines[1][0][1] * 100)
            time_lines.append(tot_lines_search)
            match_lines.append(good_perc_lines)

            print '********************'
            print 'LINE SEARCH'
            print 'test case: ' + str(i + 1)
            print 'ratio title: ' + (str(book_details_lines[1][0][0] *
                                     100) + '%')
            print 'ration author: ' + (str(book_details_lines[1][0][1] *
                                       100) + '%')
            print 'precision image match: ' + str(good_perc_lines) + '%'
            print 'time: ' + str(tot_lines_search) + ' millisecond'
            if (book_details_lines[1][0][0] > 0.5 and
                    book_details_lines[1][0][1] > 0.5 and
                    good_perc_lines/100 > 0.4):
                print 'GOOD lines match'
            else:
                print 'BAD lines match'
            if title_test != row[0] and author_test != row[1]:
                print title_test, author_test
    # print 'book number'
    # print book_number
    # print 'title blocks'
    # print title_blocks
    # print 'author blocks'
    # print author_blocks
    # print 'time blocks'
    # print time_blocks
    # print 'SIFT blocks'
    # print match_blocks
    # print 'title lines'
    # print title_lines
    # print 'author lines'
    # print author_lines
    # print 'time lines'
    # print time_lines
    # print 'SIFT lines'
    # print match_lines
    # plot blocks match
    plt.plot(book_number, title_blocks)
    plt.ylabel('title blocks ratio')
    plt.show()
    plt.plot(book_number, author_blocks)
    plt.ylabel('author blocks ratio')
    plt.show()
    plt.plot(book_number, time_blocks)
    plt.ylabel('time blocks (millisecond)')
    plt.show()
    plt.plot(book_number, match_blocks)
    plt.ylabel('sift blocks ratio')
    plt.show()
    # plot lines match
    plt.plot(book_number, title_lines)
    plt.ylabel('title lines ratio')
    plt.show()
    plt.plot(book_number, author_lines)
    plt.ylabel('author lines ratio')
    plt.show()
    plt.plot(book_number, time_lines)
    plt.ylabel('time lines millisecond')
    plt.show()
    plt.plot(book_number, match_lines)
    plt.ylabel('sift lines ratio')
    plt.show()


run_test(test_CSV_negative)
run_test(test_CSV_positive)