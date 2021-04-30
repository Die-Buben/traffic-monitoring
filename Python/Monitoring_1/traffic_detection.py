import cv2
import numpy as np

capture = cv2.VideoCapture("car_bridge.mp4")
objectDetector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=400, detectShadows=True)
kernel = np.ones((5, 5), np.uint8)
counter = 0

while True:
    _, frame = capture.read()
    regionOfInterest = frame[180:, 250:1100]  # height and width
    mask = objectDetector.apply(regionOfInterest)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)  # remove grey elements from mask, like shadows
    dilated = cv2.dilate(mask, kernel, iterations=7)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        hull = cv2.convexHull(contours[i])
        cv2.drawContours(mask, [hull], -1, (255, 0, 0), -1)

    contours2Iteration, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # get the new contours after blur
    for i in range(len(contours2Iteration)):
        hull = cv2.convexHull(contours2Iteration[i])
        cv2.drawContours(mask, [hull], -1, (255, 0, 0), -1)

    cv2.line(regionOfInterest, (0, 200), (1100, 200), (0, 0, 255), 2)

    contours3Iteration, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # get the new contours for detection
    for cnt in contours3Iteration:
        (x, y, w, h) = cv2.boundingRect(cnt)

        if w > 20 and h > 20:
            cv2.rectangle(mask, (x, y), (x+w, y+h), (255, 0, 0), 1)

            x1 = w / 2
            y1 = h / 2

            cx = x + x1
            cy = y + y1

            centroid = (cx, cy)
            cv2.circle(regionOfInterest, (int(cx), int(cy)), 10, (0, 0, 255), -1)
            if centroid > (27, 38) and centroid < (134, 108):
                counter += 1
                # https://www.semicolonworld.com/question/54759/counting-cars-opencv-python-issue

            cv2.putText(mask, str(counter), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    cv2.imshow("roi", regionOfInterest)
    cv2.imshow("mask", mask)
    #cv2.imshow("tt", dilated)
    key = cv2.waitKey(30)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
