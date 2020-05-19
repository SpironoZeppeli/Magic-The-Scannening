import cv2 as cv2
import numpy as np
import os
import pickle
import copyreg


class ImageData:
    name = None
    image = None
    keypoints = None
    descriptors = None
    good_matches = None
    set_id = None


class SetImages:
    images = []


set_images = SetImages()

detector = cv2.ORB_create(2000, 1.2)

set_file_num = 0
images = []

# While the information below is hard coded to work only with Shadows Over Innistrad (SOI), it will later
# be changed to work with other sets from the game.

for index, set_file in enumerate(os.listdir(".\\SOI")):
    print(index)
    print(set_file)
    images.append(ImageData())
    images[index - (15 * set_file_num)].image = cv2.imread(".\\SOI\\" + set_file)
    images[index - (15 * set_file_num)].keypoints, images[
        index - (15 * set_file_num)].descriptors = detector.detectAndCompute(images[index - (15 * set_file_num)].image,
                                                                             None)
    images[index - (15 * set_file_num)].set_id = 'SOI'
    images[index - (15 * set_file_num)].name = os.path.splitext(set_file)[0]
    if (index != 0 and (index + 1) % 15 == 0) or index == (len(os.listdir(".\\SOI")) - 1):
        set_images.images = images
        with open('.\\setFiles\\SOI\\setFile' + str(set_file_num), 'wb') as set_file:
            pickle.dump(set_images, set_file, -1)
        set_file_num += 1
        set_images.images = []
        images = []
