import cv2 as cv2
import numpy as np
import os
import pickle
import time
from pydobot import Dobot
from serial.tools import list_ports
from PyQt5.QtWidgets import QApplication, QLabel

# port = 'COM4'
# device = Dobot(port=port)

cap = cv2.VideoCapture(1)


class ImageData:
    name = None
    image = None
    keypoints = None
    descriptors = None
    good_matches = None
    cardId = None


class SetImages:
    images = []


def loadFiles():
    images = []
    for index, setFile in enumerate(os.listdir("../setFiles/SOI")):
        setFile = open(".\setFiles\SOI\\" + setFile, 'rb')
        setImages = pickle.load(setFile)
        setFile.close()
        for image in setImages.images:
            images.append(image)
    return images


images = None
images = loadFiles()

cameraImage = cap.read()[1]

matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)

minHessian = 400
detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)

keypointsCam, descriptorsCam = detector.detectAndCompute(cameraImage, None)

for index, image in enumerate(images):
    ##    images[index] = [image, detector.detectAndCompute(image, None)]
    print(index)
    timeStart = time.time()
    knn_matches = matcher.knnMatch(image.descriptors, descriptorsCam, 2)

    ratio_thresh = 0.7
    image.good_matches = []
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            image.good_matches.append(m)
#    print(time.time() - timeStart)


bestMatch = images[0]
for image in images:
    if (len(image.good_matches) > len(bestMatch.good_matches)):
        bestMatch = image

img_matches = np.empty(
    (max(bestMatch.image.shape[0], bestMatch.image.shape[0]), bestMatch.image.shape[1] + cameraImage.shape[1], 3),
    dtype=np.uint8)
img3 = cv2.drawMatches(bestMatch.image, bestMatch.keypoints, cameraImage, keypointsCam, bestMatch.good_matches,
                       img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# (x, y, z, r, j1, j2, j3, j4) = device.pose()
# print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
# device.move_to(x + 90, y, z - 60, r, 0x00)
# device.suck(True)
# device.move_to(x - 150, y + 200, z, r, 0x00)
# device.suck(False)
# device.move_to(x, y, z, r, 0x01)
#
# device.close()

cv2.imwrite("../image2.png", img3)
listFile = open("cardList.txt", 'a')
listFile.write(bestMatch.name + ", ")
listFile.close()
cv2.imshow('Good Matches', img3)

cv2.waitKey(0)
cv2.destroyAllWindows()