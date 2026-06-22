import os
import sys

#exe文件和py文件，图片路径拼接
if hasattr(sys,'frozen'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR,"image")

def getImage(imgName):
    return os.path.join(IMAGE_DIR,imgName)

#食物列表
FOOD = ["DynamicFluid","LicoriceDNA","Cupcakes","Cookies","Breads","Donuts","IceCream","Pizza","Pie","Turkey","Cake","BigSalad"]