import cv2
import numpy as np

from EuclideanDistanceTracker import *


def setup():
    # Make sure to adapt parameters based on the used source
    capture = cv2.VideoCapture("videoSamples/car_bridge.mp4")  # "videoSamples/Sample_1.avi"

    object_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=400, detectShadows=True)
    # Alternative parameters for different sources:
    #   Sample_1 parameters= history=500, varThreshold=1000, detectShadows=True
    #   car_bridge parameters= history=500, varThreshold=400, detectShadows=True

    tracker = EuclideanDistTracker()
    monitoring(object_detector, capture, tracker)

    capture.release()
    cv2.destroyAllWindows()


def monitoring(object_detector, capture, tracker):
    _, frame = capture.read()  # Read the first image of the source
    r = cv2.selectROI(frame, _)  # Select region of interest
    cv2.destroyAllWindows()

    while True:
        _, frame = capture.read()  # Continuously read images from source
        region_of_interest = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]  # Apply selected roi
        mask = object_detector.apply(region_of_interest)  # Generate a mask based on 'object_detector'
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)  # Remove grey elements from mask, like shadows

        pre_processing(mask)
        track_vehicle(mask, region_of_interest, tracker)

        cv2.imshow("Traffic Detection", region_of_interest)
        cv2.imshow("Mask after preprocessing", mask)

        key = cv2.waitKey(30)
        if key == 27:
            break


def pre_processing(mask):
    # Alternative parameters for different sources:
    #   Sample_1 parameters= kernel 3, 3; iterations=3
    #   car_bridge parameters= kernel 5, 5; iterations=6

    kernel = np.ones((5, 5), np.uint8)  # Kernel used for morphological operation
    dilated = cv2.dilate(mask, kernel, iterations=6)  # Morphological operation to fade over gaps in the mask
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        hull = cv2.convexHull(contours[i])
        cv2.drawContours(mask, [hull], -1, (255, 0, 0), -1)


def track_vehicle(mask, region_of_interest, tracker):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_NONE)  # Get new contours for detection
    detections = []
    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Specify the needed area to be detected as an object
        if area > 10000:
            (x, y, w, h) = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

            x1 = w / 2
            y1 = h / 2

            cx = x + x1
            cy = y + y1

            cv2.circle(region_of_interest, (int(cx), int(cy)), 10, (0, 0, 255), -1)

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, object_id = box_id
        cv2.putText(region_of_interest, str(object_id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(region_of_interest, (x, y), (x + w, y + h), (0, 255, 0), 3)


# Entry point for the script
setup()
