import cv2 as cv2
import numpy as np
import os
import pickle
import time


class ImageData:
    image = None
    keypoints = None
    descriptors = None
    good_matches = None


class SetImages:
    images = []


images = []
for index, setFile in enumerate(os.listdir("../setFiles/SOI")):
    setFile = open(".\setFiles\SOI\\" + setFile, 'rb')
    setImages = pickle.load(setFile)
    setFile.close()
    for image in setImages.images:
        images.append(image)

cameraImage = cv2.imread("porttowncam.png")

matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)

minHessian = 400
detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)

keypointsCam, descriptorsCam = detector.detectAndCompute(cameraImage, None)

for index, image in enumerate(images):
    ##    images[index] = [image, detector.detectAndCompute(image, None)]
    timeStart = time.time()
    knn_matches = matcher.knnMatch(image.descriptors, descriptorsCam, 2)

    ratio_thresh = 0.7
    image.good_matches = []
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            image.good_matches.append(m)
    print(time.time() - timeStart)

bestMatch = images[0]
for image in images:
    if (len(image.good_matches) > len(bestMatch.good_matches)):
        bestMatch = image

img_matches = np.empty(
    (max(bestMatch.image.shape[0], bestMatch.image.shape[0]), bestMatch.image.shape[1] + cameraImage.shape[1], 3),
    dtype=np.uint8)
img3 = cv2.drawMatches(bestMatch.image, bestMatch.keypoints, cameraImage, keypointsCam, bestMatch.good_matches,
                       img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv2.imwrite("../image2.png", img3)
cv2.imshow('Good Matches', img3)

cv2.waitKey(0)
cv2.destroyAllWindows()