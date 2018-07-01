import os
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys

# TODO: decide the pair (distance_coef,good_percentage) to establish if
# the two images contain the same book: at the moment (0,9,35%),
# GEB_bad non conta

# TODO: compare different tecniques

# The two honest comparisons between the same books are (GoT3,GoT3_1)
# and (GEB,GEB_photo)


queriesPath = 'src/Book_Covers/Query/'
imagesPath = 'src/Book_Covers/Images/'

distance_coef = 0.90                    # before the value was 0.75

# FLANN matcher
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params, search_params)

# BF matcher
bf = cv.BFMatcher()


def ORB_match():
    for query in os.listdir(queriesPath):
        for image in os.listdir(imagesPath):

            queryPath = queriesPath + query
            imagePath = imagesPath + image

            img1 = cv.imread(queryPath, 0)          # queryImage
            img2 = cv.imread(imagePath, 0)          # trainImage

            # Initiate ORB detector
            orb = cv.ORB_create()
            # find the keypoints and descriptors with ORB
            kp1, des1 = orb.detectAndCompute(img1, None)
            kp2, des2 = orb.detectAndCompute(img2, None)
            # Match descriptors.
            matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
            matches = matcher.match(des1, des2)
            # Sort them in the order of their distance.
            matches = sorted(matches, key=lambda x: x.distance)
            print
            print '***********'
            print 'query:', query
            print 'image:', image
            print

            print 'descriptors image 1:',  len(des1)
            print 'descriptors image 2:', len(des2)
            print 'good:', len(matches)
            print 'good percentage: ' + str(len(matches) * 100.0 / len(des1)) + '%'
            # cv.drawMatchesKnn expects list of lists as matches.
            # img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2,
            #                          good, flags=2, outImg=None)
            # plt.imshow(img3), plt.show()


def sift_match(matcher):
    """
    matcher can be: brute-force or flann.
    Type:
    sift_match(bf)
    sift_martch(flann)
    """             # before the value was 0.75

    for query in os.listdir(queriesPath):
        for image in os.listdir(imagesPath):

            # query     = 'GEB.jpg'
            # query     = 'GoT3.jpg'
            # image     = 'GoT3_1.jpg'
            # image     = 'GEB_bad.jpg'

            queryPath = queriesPath + query
            imagePath = imagesPath + image

            img1 = cv.imread(queryPath, 0)          # queryImage
            img2 = cv.imread(imagePath, 0)          # trainImage
            # Initiate SIFT detector
            sift = cv.xfeatures2d.SIFT_create()
            # find the keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(img1, None)
            kp2, des2 = sift.detectAndCompute(img2, None)
            # BFMatcher with default params
            matches = matcher.knnMatch(des1, des2, k=2)
            # Apply ratio test
            good = []

            for m, n in matches:
                if m.distance < distance_coef * n.distance:
                    good.append([m])

            print
            print '***********'
            print 'query:', query
            print 'image:', image
            print

            print 'descriptors image 1:',  len(des1)
            print 'descriptors image 2:', len(des2)
            print 'good:', len(good)
            print 'good percentage: ' + str(len(good) * 100.0 / len(des1)) + '%'
            # cv.drawMatchesKnn expects list of lists as matches.
            # img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2,
            #                          good, flags=2, outImg=None)
            # plt.imshow(img3), plt.show()


def surf_match(matcher):
    """
    matcher can be: brute-force or flann.
    Type:
    sift_match(bf)
    sift_martch(flann)
    """             # before the value was 0.75

    for query in os.listdir(queriesPath):
        for image in os.listdir(imagesPath):

            # query     = 'GEB.jpg'
            # query     = 'GoT3.jpg'
            # image     = 'GoT3_1.jpg'
            # image     = 'GEB_bad.jpg'

            queryPath = queriesPath + query
            imagePath = imagesPath + image

            img1 = cv.imread(queryPath, 0)          # queryImage
            img2 = cv.imread(imagePath, 0)          # trainImage
            # Initiate SIFT detector
            surf = cv.xfeatures2d.SURF_create()
            # find the keypoints and descriptors with surf
            kp1, des1 = surf.detectAndCompute(img1, None)
            kp2, des2 = surf.detectAndCompute(img2, None)
            # BFMatcher with default params
            matches = matcher.knnMatch(des1, des2, k=2)
            # Apply ratio test
            good = []

            for m, n in matches:
                if m.distance < distance_coef * n.distance:
                    good.append([m])

            print
            print '***********'
            print 'query:', query
            print 'image:', image
            print

            print 'descriptors image 1:',  len(des1)
            print 'descriptors image 2:', len(des2)
            print 'good:', len(good)
            print 'good percentage: ' + str(len(good) * 100.0 / len(des1)) + '%'
            # cv.drawMatchesKnn expects list of lists as matches.
            # img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2,
            #                          good, flags=2, outImg=None)
            # plt.imshow(img3), plt.show()


# brute_force_match()
# sift_match(bf)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print
        print 'Usage: python src/areSimilar.py \
<sift | surf | orb> <bf | flann>'
    elif sys.argv[1] == 'sift':
        if sys.argv[2] == 'bf':
            print 'sift bf'
            sift_match(bf)
        else:
            print 'sift flann'
            sift_match(flann)
    elif sys.argv[1] == 'surf':
        if sys.argv[2] == 'bf':
            print 'surf bf'
            surf_match(bf)
        else:
            print 'surf flann'
            surf_match(flann)
    elif sys.argv[1] == 'orb':
        if sys.argv[2] == 'bf':
            print 'orb bf'
            ORB_match()
        else:
            print 'orb flann (not already implemented)'
            # ORB_match(flann)
    else:
        print
        print 'Usage: python src/areSimilar.py \
<sift | surf | orb> <bf | flann>'
