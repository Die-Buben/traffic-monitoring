import tkinter as tk
import VideoProcessing


class Userinterface(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #  self.master = master
        self.pack()
        self.create_widgets()
        self.create_text_view()

    def create_widgets(self):
        self.btn_monitoring = tk.Button(self)
        self.btn_monitoring["text"] = "Start the monitoring!"
        self.btn_monitoring["command"] = self.start_monitoring
        self.btn_monitoring.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.display = tk.Label(self, text="Hallo")
        self.display.pack()

    def create_text_view(self):
        self.car_counter = tk.Text(self)
        self.car_counter.insert('end', "Testtext für das TextView")
        self.car_counter.pack(side="top")

    def update_car_amount(self, car_amount="HA"):
        self.display.configure(text=car_amount)
        self.display.pack()

    def start_monitoring(self):
        #  monit = VideoProcessing.VideoProcessing("videoSamples/car_bridge.mp4")
        monit = VideoProcessing.VideoProcessing("http://192.168.178.34:8080/video")
        monit.setup()