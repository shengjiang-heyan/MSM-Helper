import pyautogui
import time
import config

class MSMbot:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

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
            "coinCollect" : config.getImage("CoinCollect.png"),
            "confirm" : config.getImage("Confirm.png"),
            "diamondCollect" : config.getImage("DiamondCollect.png"),
            "foodCollect" : config.getImage("FoodCollect.png"),
            "setting" : config.getImage("Setting.png"),
            "coin" : config.getImage("Coin.png")
        }

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
            time.sleep(1)

    def toIsland(self,island):
        #打开地图
        pos = self.findImage(self.images["map"],"Map",self.conf,5)
        if pos:
            pyautogui.click(pos)
        pos = self.findImage(self.images["no"],"No",self.conf,20)

        #选岛
        for _ in range(5):
            pos = self.findImage(config.getImage("island/"+island+".png"),island,self.conf,0.5)
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

    def collectCoinFast(self):
        for attempt in range(2):
            pos = self.findImage(self.images["coinCollect"],"CoinCollect",self.conf,5)
            if pos:
                pyautogui.click(pos)
                time.sleep(1)
                pos = self.findImage(self.images["confirm"],"Confirm",self.conf,5)
                if pos:
                    pyautogui.click(pos)
                    print("完成 一键收集金币")
                    return True
                else:
                    self.closeAd()
        print("失败 一键收集金币")
        return False


    def collectResource(self,imgKey,name,maxTry,postDelay):
        for attempt in range(maxTry):
            pos = self.findImage(self.images[imgKey],name,self.conf,0.5)
            if pos:
                pyautogui.click(pos)
                print(f"收集 {name}: {attempt+1}")
            elif not pos and attempt > 0:
                print(f"完成收集 {name}")
                return True
            else:
                print(f"没有 {name}")
                return True
            time.sleep(postDelay)
        print("超出最大尝试限制")
        return False

    def run(self):
        time.sleep(3)
        self.closeAd()
        for island in self.islands:
            print(f"------ 前往岛屿：{island} ------")
            self.toIsland(island)
            time.sleep(2)
            print()
            print(f"------ 收取金币 ------")
            self.collectCoinFast()
            time.sleep(2)
            print(f"------ 收取钻石 ------")
            self.collectResource("diamondCollect","Diamond",1,0.5)
            time.sleep(1)
            print(f"------ 收取食物 ------")
            self.collectResource("foodCollect","Food",5,0.5)
            time.sleep(1)