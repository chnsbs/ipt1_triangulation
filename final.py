__author__ = 'mlm-cs'

import tkintertable
import linedetection
import matplotlib.pyplot as plt
from Tkinter import *
import threading

if __name__ == '__main__':

    mygui = tkintertable.Application()
    detection = linedetection.linedetection()
    detection.setName('Line Detection Thread')
    mygui.getLineDetectionInstance(detection)
    mygui.start()
    mygui.root.mainloop()









