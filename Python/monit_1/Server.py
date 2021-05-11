from flask import Flask, render_template, Response
import cv2


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.camera = cv2.VideoCapture("http://192.168.178.34:8080/video")  # '("http://192.168.178.34:8080/video")  # use 0 for web camera

    def gen_frames(self):  # generate frame by frame from camera
        while True:
            # Capture frame-by-frame
            success, frame = self.camera.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def run(self):
        app = self.app

        @app.route('/video_feed')
        def video_feed():
            # Video streaming route. Put this in the src attribute of an img tag
            return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')

        app.run() #("192.168.178.131", debug=True)