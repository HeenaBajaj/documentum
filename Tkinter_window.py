from tkinter import *


def createwindow(name,w,h):
    root = Tk()
    root.title(name)
    # root.geometry("1200x1200")

    # w = 300 # width for the Tk root
    # h = 300 # height for the Tk root

    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.attributes('-fullscreen', False)
    return root