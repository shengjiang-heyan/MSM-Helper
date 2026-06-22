import pyautogui
import time
import config
import threading

class ForceStop(Exception):
    pass

class MSMbot:
    def __init__(self,stopEvent:threading.Event):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.2

        self.stopEvent = stopEvent
        self.wid,self.hei = pyautogui.size()
        self.conf = 0.8

        self.islands = [
            "Plant","Cold","Air","Water","Fire","Shugabush",
            "Ethereal","Workshop","Haven","Oasis","Mythical",
            "Light","Psychic","Faerie","Bone","Sanctum",
            "Wublin","Celestial"
        ]

        self.images = {
            "advertisement" : config.getImage("Advertisement.png"),
            "map" : config.getImage("map.png"),
            "go" : config.getImage("Go.png"),
            "youAreHere" : config.getImage("YouAreHere.png"),
            "back" : config.getImage("Back.png"),
            "no" : config.getImage("No.png"),
            "setting" : config.getImage("Setting.png")
        }

    def botSleep(self,duration):
        for _ in range(int(duration * 2)):
            if self.stopEvent.is_set():
                raise ForceStop("程序中断运行")
            time.sleep(0.5)

    def findImage(self,imgPath,name,confid,timeLimit):
        startTime = time.time()
        while (time.time()-startTime < timeLimit):
            try:
                pos = pyautogui.locateOnScreen(imgPath,confidence=confid)
                print(f"识别到：{name}")
                return pos
            except pyautogui.ImageNotFoundException:
                pass
        print(f"未识别到：{name}")
        return None

    def closeAd(self):
        pos = self.findImage(self.images["advertisement"],"Close Advertisement",self.conf,0.5)
        if pos:
            pyautogui.click(pos)

    def toIsland(self,island):
        #打开地图
        pos = self.findImage(self.images["map"],"Map",self.conf,5)
        if pos:
            pyautogui.click(pos)
        pos = self.findImage(self.images["no"],"No",self.conf,20)

        #选岛
        for _ in range(10):
            pos = self.findImage(config.getImage(f"island/{island}.png"),island,self.conf,0.5)
            if pos:
                pyautogui.click(pos)
                break
            pyautogui.moveTo(self.wid/10,self.hei/2)
            if island == "Plant":
                pyautogui.scroll(1000)
            else:
                pyautogui.scroll(-200)

        #前往岛
        for _ in range(10):
            pos = self.findImage(self.images["go"],"Go",self.conf,0.5)
            if pos:
                pyautogui.click(pos)
                break
            pos = self.findImage(self.images["youAreHere"],"YouAreHere",self.conf,0.5)
            if pos:
                pos = self.findImage(self.images["back"],"Back",self.conf,5)
                if pos:
                    pyautogui.click(pos)
                    pos = self.findImage(self.images["no"],"No",self.conf,5)
                    if pos:
                        pyautogui.click(pos)
                        break
        pos = self.findImage(self.images["setting"],"setting",self.conf,20)
        if pos:
            return True
        else:
            return False

