import cv2 as cv2
import numpy as np
import os
import pickle
import copyreg


class ImageData:
    image = None
    keypoints = None
    descriptors = None
    good_matches = None


class SetImages:
    images = []


def _pickle_keypoints(point):
    return cv2.KeyPoint, (*point.pt, point.size, point.angle,
                          point.response, point.octave, point.class_id)


copyreg.pickle(cv2.KeyPoint().__class__, _pickle_keypoints)

setImages = SetImages()
minHessian = 400
detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)

setFileNum = 0
images = []
for index, file in enumerate(os.listdir("../SOI")):
    print(index)
    print(file)
    images.append(ImageData())
    images[index - (15 * setFileNum)].image = cv2.imread(".\SOI\\" + file)
    images[index - (15 * setFileNum)].keypoints, images[
        index - (15 * setFileNum)].descriptors = detector.detectAndCompute(images[index - (15 * setFileNum)].image,
                                                                           None)
    if (index != 0 and (index + 1) % 15 == 0):
        setImages.images = images
        with open('.\setFiles\SOI\setFile' + str(setFileNum), 'wb') as file:
            pickle.dump(setImages, file, -1)
        setFileNum += 1
        setImages.images = []
        images = []



