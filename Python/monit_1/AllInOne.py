import numpy as np
from flask import Flask, render_template, Response, request
import cv2

from EuclideanDistanceTracker import EuclideanDistTracker


class AllInOne():
    def __init__(self, source_path="videoSamples/car_bridge.mp4"):
        self.app = Flask(__name__)
        self.__source_path = source_path
        self.__capture = cv2.VideoCapture(self.__source_path)
        self.__tracker = EuclideanDistTracker()
        self.__bgs_history = 500
        self.__bgs_treshold = 128  # Mögliche Wertebereiche suchen und überprüfen. Evtl. umgehen der convex
        self.__bgs_detect_shadows = True
        self.__preprocessing_mat_size = 5
        self.__preprocessing_iterations = 6
        self.__tracking_area = 10000
        self.__region_of_interest = 0
        self.__mask = 0

    def setup(self):  # Nicht verwendet
        object_detector = cv2.createBackgroundSubtractorMOG2(history=self.__bgs_history,
                                                             varThreshold=self.__bgs_treshold,
                                                             detectShadows=self.__bgs_detect_shadows)
        self.__monitoring(object_detector)

        self.__capture.release()
        cv2.destroyAllWindows()

    def __monitoring(self, object_detector):
        _, frame = self.__capture.read()
        r = cv2.selectROI("selectRoi", frame)
        cv2.destroyWindow("selectRoi")
        while True:
            _, frame = self.__capture.read()
            self.__region_of_interest = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            self.__mask = object_detector.apply(self.__region_of_interest)
            _, self.__mask = cv2.threshold(self.__mask, 254, 255, cv2.THRESH_BINARY)

            self.__pre_processing()
            self.__track_vehicle()

            # cv2.imshow("Traffic Detection", self.__region_of_interest)
            # cv2.imshow("Mask after preprocessing", self.__mask)

            _, buffer = cv2.imencode('.jpg', self.__region_of_interest)
            self.__region_of_interest = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + self.__region_of_interest + b'\r\n')  # concat frame one by one and show result

    def __pre_processing(self):
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(self.__mask, kernel, iterations=self.__preprocessing_iterations)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for i in range(len(contours)):
            hull = cv2.convexHull(contours[i])
            cv2.drawContours(self.__mask, [hull], -1, (255, 0, 0), -1)

    def __track_vehicle(self):
        contours, _ = cv2.findContours(self.__mask, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_NONE)  # get the new contours for detection
        detections = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > self.__tracking_area:
                (x, y, w, h) = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

                x1 = w / 2
                y1 = h / 2

                cx = x + x1
                cy = y + y1

                cv2.circle(self.__region_of_interest, (int(cx), int(cy)), 10, (0, 0, 255), -1)

        boxes_ids = self.__tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cv2.putText(self.__region_of_interest, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(self.__region_of_interest, (x, y), (x + w, y + h), (0, 255, 0), 3)

    def run(self):
        app = self.app
        object_detector = cv2.createBackgroundSubtractorMOG2(history=self.__bgs_history,
                                                             varThreshold=self.__bgs_treshold,
                                                             detectShadows=self.__bgs_detect_shadows)
        self.__monitoring(object_detector)

        @app.route('/video_feed')
        def video_feed():
            # Video streaming route. Put this in the src attribute of an img tag
            return Response(self.__monitoring(object_detector), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')

        @app.route('/settings')
        def settings():
            return "Settings"

        app.run("192.168.178.131", debug=True)