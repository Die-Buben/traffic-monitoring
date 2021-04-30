import cv2
import numpy as np

from tracker import *

# https://www.youtube.com/watch?v=O3b8lVF93jU&list=RDCMUC5hHNks012Ca2o_MPLRUuJw&start_radio=1 min 16

#cap = cv2.VideoCapture("Sample_2_MP4.mp4")
cap = cv2.VideoCapture("car_bridge.mp4")

tracker = EuclideanDistTracker()

# Object detection for stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=250, varThreshold=150, detectShadows=True)
 # the longer the history, the better the detection

while True:
    ret, frame = cap.read()

    #Extract region of interest
    regionOfInterest = frame[100: 1000, 500: 1500] #height, width
    #evtl über funktion einzelne Pixelbereiche (kleinere) der regOI hinzufügen und
    # nicht über Listenbereiche


    #Object detection
    mask = object_detector.apply(regionOfInterest)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY) #remove grey elements from mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    hull_list = []

    for i in range(len(contours)):
        hull_list.append(cv2.convexHull(contours[i], False))

    drawing_convex = np.zeros((mask.shape[0], mask.shape[1], 3), np.uint8)

    for i in range(len(contours)):
        cv2.drawContours(drawing_convex, hull_list, i, (0, 255, 0), 3)

    for cnt in contours:
        #Calculate Area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 1000: #Use this to determine the size of the vehilce 35000 for bedroom
            #cv2.drawContours(regionOfInterest, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])
            cv2.drawContours(regionOfInterest, hull_list, -1, (0, 255, 0), 3)
            cv2.rectangle(regionOfInterest, (x, y), (x + w, y + h), (0, 255, 0))


    #Object tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        #cv2.putText(regionOfInterest, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        #cv2.rectangle(regionOfInterest, (x, y), (x + w, y + h), (0, 255, 0))

    #cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    #cv2.imshow("RegionofInterest", regionOfInterest)
    #cv2.imshow("hh", drawing_convex)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
