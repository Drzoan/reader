from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np

import cv2
import imutils
import os


def transform_coord(filepath, coords):
    image = cv2.imread(filepath)
    pts = np.array(eval(coords), dtype="float32")
    warped = four_point_transform(image, pts)
    cv2.imshow("Original", image)
    cv2.imshow("Warped", warped)
    cv2.waitKey(0)


def transform_guess(filepath):
    image = cv2.imread(filepath)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edge = cv2.Canny(gray, 75, 200)

    cnts = cv2.findContours(edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
        if len(approx) == 4:
            screenCnt = approx
            break

    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    final = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    final = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    T = threshold_local(final, 11, offset=10, method="gaussian")
    final = (final > T).astype("uint8") * 255

    filename = os.path.basename(filepath)
    cv2.imwrite(filename, final)
    cv2.waitKey(0)



