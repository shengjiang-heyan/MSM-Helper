import os
import sys
import pyautogui
import time

logPath = "gameLog.txt"
sys.stdout = open(logPath,"a",encoding="utf-8")

def getPath(path):
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,path)
    return os.path.join(os.path.abspath("."),path)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

advertisementImg = getPath("image/Advertisement.png")
map1Img = getPath("image/map1.png")
map2Img = getPath("image/map2.png")
goImg = getPath("image/Go.png")
youAreHereImg = getPath("image/YouAreHere.png")
backImg = getPath("image/Back.png")
noImg = getPath("image/No.png")
coinCollectImg = getPath("image/CoinCollect.png")
confirmImg = getPath("image/Confirm.png")
diamondCollectImg = getPath("image/DiamondCollect.png")
foodCollectImg = getPath("image/FoodCollect.png")

wid,hei = pyautogui.size()

conf = 0.8
longPause = 5
midPause = 3

time.sleep(3)

islands = ["Plant","Cold","Air","Water","Fire","Shugabush","Ethereal","Workshop","Haven","Oasis","Mythical","Light","Psychic","Faerie","Bone","Sanctum","Wublin","Celestial"]

try:
    pos = pyautogui.locateOnScreen(advertisementImg,confidence=conf)
    print(pos)
    pyautogui.click(pos)
    print("Close Advertisement")
except pyautogui.ImageNotFoundException:
    print("No Advertisement")

time.sleep(midPause)

for island in islands:
    print("Map")
    #打开地图
    try:
        pos = pyautogui.locateOnScreen(map1Img,confidence=conf)
        pyautogui.click(pos)
        print("Success Map")
    except pyautogui.ImageNotFoundException:
        try:
            pos = pyautogui.locateOnScreen(map2Img,confidence=conf)
            pyautogui.click(pos)
            print("Success Map")
        except pyautogui.ImageNotFoundException:
            print("Fail Map")

    time.sleep(longPause)

    #选岛
    print(island + "\n")
    for tryTime in range(5):
        try:
            pos = pyautogui.locateOnScreen(getPath("image/island/"+island+".png"),confidence=conf)
            pyautogui.click(pos)
            print("Success " + island)
            break
        except pyautogui.ImageNotFoundException:
            pyautogui.moveTo(wid/10,hei/2)
            if island == "Plant":
                pyautogui.scroll(1000)
            else:
                pyautogui.scroll(50)
            print(island + "Fail " + str(tryTime))

    time.sleep(midPause)

    #前往岛
    try:
        pos = pyautogui.locateOnScreen(goImg,confidence=conf)
        pyautogui.click(pos)
        print("Success Go")
    except pyautogui.ImageNotFoundException:
        print("Fail Go")

    try:
        pos = pyautogui.locateOnScreen(youAreHereImg,confidence=conf)
        pos = pyautogui.locateOnScreen(backImg,confidence=conf)
        pyautogui.click(pos)

        time.sleep(midPause)
        pos = pyautogui.locateOnScreen(noImg,confidence=conf)
        pyautogui.click(pos)
        print("Success YouAreHere")
    except pyautogui.ImageNotFoundException:
        print("Fail YouAreHere")

    time.sleep(longPause)

    #关广告
    try:
        pos = pyautogui.locateOnScreen(advertisementImg,confidence=conf)
        print(pos)
        pyautogui.click(pos)
        print("Close Advertisement")
    except pyautogui.ImageNotFoundException:
        print("No Advertisement")

    time.sleep(midPause)

    #金币
    print("Coin")
    try:
        pos = pyautogui.locateOnScreen(coinCollectImg,confidence=conf)
        pyautogui.click(pos)
        time.sleep(2)
        try:
            pos = pyautogui.locateOnScreen(confirmImg,confidence=conf)
            pyautogui.click(pos)
            print("Success Coin")
        except pyautogui.ImageNotFoundException:
            print("Fail Coin")
    except pyautogui.ImageNotFoundException:
        print("Fail Coin")

    time.sleep(longPause)

    #钻石
    print("Diamond")
    try:
        pos = pyautogui.locateOnScreen(diamondCollectImg,confidence=conf)
        pyautogui.click(pos)
        print("Success Diamond")
    except pyautogui.ImageNotFoundException:
        print("Fail Diamond")

    time.sleep(midPause)

    #食物
    print("Food")
    for i in range(5):
        try:
            pos = pyautogui.locateOnScreen(foodCollectImg, confidence=conf)
            pyautogui.click(pos)
            print("Success Food")
        except pyautogui.ImageNotFoundException:
            print("Fail Food")
            break
        time.sleep(midPause)

    time.sleep(midPause)
