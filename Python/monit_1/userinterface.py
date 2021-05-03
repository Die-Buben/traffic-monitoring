import tkinter as tk
import monitoring


def start_monitoring():
    monitoring.setup()


def say_hi():
    print("hi there, everyone!")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.create_text_view()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Start the monitoring!"
        self.hi_there["command"] = start_monitoring
        #self.hi_there["command"] = say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def create_text_view(self):
        self.car_conter = tk.Text(self)
        self.car_conter.insert('end', "Testtext für das TextView")
        self.car_conter.pack(side="top")


'''
from tkinter import *


def printInfo():
    print("Hi")


root = Tk()
root.geometry('300x150')

myLabel = Label(root, text="Traffic Detection")

btn = Button(root, text="Button: printInfo()")
myLabel.pack()
btn.pack()
root.mainloop()
'''


