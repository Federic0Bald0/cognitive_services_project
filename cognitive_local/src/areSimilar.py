import os
import numpy as np
import cv2
from matplotlib import pyplot as plt

# TODO: decide the pair (distance_coef,good_percentage) to establish if
# the two images contain the same book: at the moment (0,9,35%), GEB_bad non conta

# TODO: compare different tecniques

# The two honest comparisons between the same books are (GoT3,GoT3_1)
# and (GEB,GEB_photo)

queriesPath = 'Book_Covers/Query/'
imagesPath = 'Book_Covers/Images/'

distance_coef = 0.9					# before the value was 0.75

for query in os.listdir(queriesPath):
	for image in os.listdir(imagesPath):

# query     = 'GEB.jpg'
# query     = 'GoT3.jpg'
# image     = 'GoT3_1.jpg'
# image     = 'GEB_bad.jpg'

		queryPath = queriesPath + query
		imagePath = imagesPath + image

		img1 = cv2.imread(queryPath,0)          # queryImage
		img2 = cv2.imread(imagePath,0)          # trainImage
		# Initiate SIFT detector
		sift = cv2.xfeatures2d.SIFT_create()
		# find the keypoints and descriptors with SIFT
		kp1, des1 = sift.detectAndCompute(img1,None)
		kp2, des2 = sift.detectAndCompute(img2,None)
		# BFMatcher with default params
		bf = cv2.BFMatcher()
		matches = bf.knnMatch(des1,des2, k=2)
		# Apply ratio test
		good = []

		for m,n in matches:
			if m.distance < distance_coef*n.distance:
				good.append([m])
				

		print 
		print '***********'
		print 'query:', query
		print 'image:', image
		print

		print 'descriptors image 1:',  len(des1)
		print 'descriptors image 2:', len(des2)     
		print 'good:', len(good)
		print 'good percentage: ' + str(len(good)*100.0/len(des1)) + '%'
		# cv2.drawMatchesKnn expects list of lists as matches.
		img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,flags=2,outImg=None)
		# plt.imshow(img3),plt.show()
