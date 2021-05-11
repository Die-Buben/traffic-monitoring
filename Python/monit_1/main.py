from AllInOne import AllInOne
from Server import *

# r = AllInOne("http://192.168.178.34:8080/video")
r = AllInOne("videoSamples/car_bridge.mp4")
r.run()


'''
root = tk.Tk()
root.title('traffic-monitoring')
app = Userinterface(root)
app.mainloop()
'''
