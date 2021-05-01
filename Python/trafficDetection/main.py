import cv2
import numpy as np
from tracker import *


def pre_processing():
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=6)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        hull = cv2.convexHull(contours[i])
        cv2.drawContours(mask, [hull], -1, (255, 0, 0), -1)


def track_vehicle():
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_NONE)  # get the new contours for detection
    detections = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10000:
            (x, y, w, h) = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

            x1 = w / 2
            y1 = h / 2

            cx = x + x1
            cy = y + y1

            cv2.circle(regionOfInterest, (int(cx), int(cy)), 10, (0, 0, 255), -1)

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(regionOfInterest, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(regionOfInterest, (x, y), (x + w, y + h), (0, 255, 0), 3)


capture = cv2.VideoCapture("videoSamples/car_bridge.mp4")

objectDetector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=400, detectShadows=True)
tracker = EuclideanDistTracker()

while True:
    _, frame = capture.read()
    regionOfInterest = frame[125:, 250:1100]  # car_bridge.mp4  //height and width
    mask = objectDetector.apply(regionOfInterest)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)  # remove grey elements from mask, like shadows

    pre_processing()
    track_vehicle()

    cv2.imshow("Traffic Detection", regionOfInterest)
    cv2.imshow("Mask after preprocessing", mask)

    key = cv2.waitKey(30)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
