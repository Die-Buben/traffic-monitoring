import cv2
import numpy as np


def version_1():
    # Load the image
    img1 = cv2.imread('car_1.PNG')
    # Convert it to greyscale
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # Threshold the image
    _, thresh = cv2.threshold(img, 110, 255, 0)
    # Find the contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # For each contour, find the convex hull and draw it
    # on the original image.
    for i in range(len(contours)):
        hull = cv2.convexHull(contours[i])
        cv2.drawContours(img, [hull], -1, (255, 0, 0), 2)
    # Display the final convex hull image
    cv2.imshow('ConvexHull', img)
    cv2.waitKey(0)

def version_2():
    src = cv2.imread("car_1.PNG", 1)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    blur = cv2.blur(gray, (3, 3))  # blur the image
    ret, thresh = cv2.threshold(blur, 110, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull = []
    for i in range(len(contours)):
        hull.append(cv2.convexHull(contours[i], False))

    drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
    for i in range(len(contours)):
        color_contours = (0, 255, 0)
        color = (255, 0, 0)
        cv2.drawContours(src, contours, i, color_contours, 1, 8, hierarchy)
        cv2.drawContours(src, hull, i, color, 1, 8)
        cv2.fillPoly(src, hull, color)

    cv2.imshow('ConvexHull', src)
    cv2.waitKey(0)


version_2()
