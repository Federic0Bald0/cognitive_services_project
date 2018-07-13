import os
import csv
import time
import cv2 as cv
import matplotlib.pyplot as plt
from src.datastore import find_book
from src.areSimilar import sift_match_images, flann, bf


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
                    good_perc_lines/100 > 0.45):
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


queriesPath = 'src/Book_Covers/Query/'
imagesPath = 'src/Book_Covers/Images/'
coef = [0.75, 0.80, 0.85, 0.90, 0.95]


def testing_sift():
    time_bf = []
    time_flann = []
    flann1 = []
    bf1 = []
    flann2 = []
    bf2 = []
    flann3 = []
    bf3 = []
    flann4 = []
    bf4 = []
    flann5 = []
    bf5 = []
    sift = cv.xfeatures2d.SIFT_create()

    for query in os.listdir(queriesPath):
        if not query.startswith('.'):
            print '**************************'
            print query
            print '**************************'
            queryPath = queriesPath + query
            img1 = cv.imread(queryPath, 0)
            best = {'0.75': ([0, 0], ['', '']),
                    '0.8': ([0, 0], ['', '']),
                    '0.85': ([0, 0], ['', '']),
                    '0.9': ([0, 0], ['', '']),
                    '0.95': ([0, 0], ['', ''])}
            time_match = [0, 0]
            for image in os.listdir(imagesPath):
                if not image.startswith('.'):
                    imagePath = imagesPath + image
                    img2 = cv.imread(imagePath, 0)

                    # Initiate SIFT detector
                    # find the keypoints and descriptors with SIFT
                    t0 = int(round(time.time() * 1000))
                    kp1, des1 = sift.detectAndCompute(img1, None)
                    kp2, des2 = sift.detectAndCompute(img2, None)
                    # matcher
                    bf_matches = bf.knnMatch(des1, des2, k=2)
                    tf_bf = int(round(time.time() * 1000))
                    flann_matches = flann.knnMatch(des1, des2, k=2)
                    tf_flann = int(round(time.time() * 1000))
                    # time
                    time_match[0] = tf_bf - t0
                    time_match[1] = tf_flann - t0
                    # good point using dinstance coef
                    for distance_coef in coef:
                        bf_good_match = []
                        for m, n in bf_matches:
                            if m.distance < distance_coef * n.distance:
                                bf_good_match.append([m])
                        flann_good_match = []
                        for m, n in flann_matches:
                            if m.distance < distance_coef * n.distance:
                                flann_good_match.append([m])

                        bf_best = len(bf_good_match) * 100.0 / len(des1)
                        flann_best = ((len(flann_good_match) * 100.0) /
                                      len(des1))

                        if best[str(distance_coef)][0][0] < bf_best:
                            best[str(distance_coef)][0][0] = bf_best
                            best[str(distance_coef)][1][0] = image

                        if (best[str(distance_coef)][0][1] < flann_best):
                            best[str(distance_coef)][0][1] = flann_best
                            best[str(distance_coef)][1][1] = image

            print 'BF time ' + str(time_match[0])
            print 'FLANN time ' + str(time_match[1])
            time_bf.append(time_match[0])
            time_flann.append(time_match[1])
            print 'Best image with differnt coefficient:'
            print '0.75'
            print 'BF ' + str(best['0.75'][0][0])
            bf1.append(best['0.75'][0][0])
            print 'BF_image ' + best['0.75'][1][0]
            print 'FLANN ' + str(best['0.75'][0][1])
            flann1.append(best['0.75'][0][1])
            print 'FLANN_image ' + best['0.75'][1][1]
            print '0.80'
            print 'BF ' + str(best['0.8'][0][0])
            bf2.append(best['0.8'][0][0])
            print 'BF_image ' + best['0.8'][1][0]
            print 'FLANN ' + str(best['0.8'][0][1])
            flann2.append(best['0.8'][0][1])
            print 'FLANN_image ' + best['0.8'][1][1]
            print '0.85'
            print 'BF ' + str(best['0.85'][0][0])
            bf3.append(best['0.85'][0][0])
            print 'BF_image ' + best['0.85'][1][0]
            print 'FLANN ' + str(best['0.85'][0][1])
            flann3.append(best['0.85'][0][1])
            print 'FLANN_image ' + best['0.85'][1][1]
            print '0.90'
            print 'BF ' + str(best['0.9'][0][0])
            bf4.append(best['0.9'][0][0])
            print 'BF_image ' + best['0.9'][1][0]
            print 'FLANN ' + str(best['0.9'][0][1])
            flann4.append(best['0.9'][0][1])
            print 'FLANN_image ' + best['0.9'][1][1]
            print '0.95'
            print 'BF ' + str(best['0.95'][0][0])
            bf5.append(best['0.95'][0][0])
            print 'BF_image ' + best['0.95'][1][0]
            print 'FLANN ' + str(best['0.95'][0][1])
            flann5.append(best['0.95'][0][1])
            print 'FLANN_image ' + best['0.95'][1][1]

    print time_bf
    print time_flann
    print bf1
    print flann1
    print bf2
    print flann2
    print bf3
    print flann3
    print bf4
    print flann4
    print bf5
    print flann5

# testing_sift()
run_test(test_CSV_negative)
run_test(test_CSV_positive)