import cv2 as cv2
import numpy as np
import os
import pickle
import time
import csv


class AppORB:
    class ImageData:
        name = None
        image = None
        keypoints = None
        descriptors = None
        good_matches = None
        set_id = None

    class SetImages:
        images = []

    def cap_image(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        ret, camera_image = cap.read()
        return camera_image

    def scan_card(self, camera_image):
        images = []
        for index, set_file in enumerate(os.listdir(".\\setFiles\\SOI")):
            set_file = open(".\\setFiles\\SOI\\{0}".format(set_file), 'rb')
            set_images = pickle.load(set_file)
            set_file.close()
            for image in set_images.images:
                images.append(image)

        if camera_image is None:
            camera_image = AppORB.cap_image(self)

        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)

        min_hessian = 400
        detector = cv2.ORB_create(2000, 1.2)

        keypoints_cam, descriptors_cam = detector.detectAndCompute(camera_image, None)

        for index, image in enumerate(images):
            time_start = time.time()

            knn_matches = matcher.knnMatch(np.float32(image.descriptors), np.float32(descriptors_cam), 2)

            ratio_thresh = 0.7
            image.good_matches = []
            for m, n in knn_matches:
                if m.distance < ratio_thresh * n.distance:
                    image.good_matches.append(m)
            print(time.time() - time_start)

        best_match = images[0]
        for image in images:
            if len(image.good_matches) > len(best_match.good_matches):
                best_match = image

        img_matches = np.empty(
            (
                max(best_match.image.shape[0], best_match.image.shape[0]),
                best_match.image.shape[1] + camera_image.shape[1],
                3),
            dtype=np.uint8)
        img3 = cv2.drawMatches(best_match.image, best_match.keypoints, camera_image, keypoints_cam,
                               best_match.good_matches,
                               img_matches)

        with open('cardList.csv', 'a+', newline='') as csvfile:
            card_writer = csv.writer(csvfile, delimiter=' ',
                                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
            card_writer.writerow(best_match.name)


        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = AppORB.scan_card(AppORB, AppORB.cap_image(AppORB))  # Does not work
