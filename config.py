import os
import sys

if hasattr(sys,'frozen'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR,"image")

def getImage(imgName):
    return os.path.join(IMAGE_DIR,imgName)