import pyautogui
import config

from core.base_bot import MSMbot

class CollectBot:
    def __init__(self,bot:MSMbot):
        self.bot = bot

        self.images = {
            "coinCollect" : config.getImage("CoinCollect.png"),
            "confirm" : config.getImage("Confirm.png"),
            "diamondCollect" : config.getImage("DiamondCollect.png"),
            "foodCollect" : config.getImage("FoodCollect.png")
        }

    def collectCoinFast(self):
        for reTry in range(2):
            pos = self.bot.findImage(self.images["coinCollect"],"CoinCollect",self.bot.conf,5)
            if pos:
                pyautogui.click(pos)
                self.bot.botSleep(1)
                pos = self.bot.findImage(self.images["confirm"],"Confirm",self.bot.conf,5)
                if pos:
                    pyautogui.click(pos)
                    print("完成 一键收集金币")
                    return True
                else:
                    self.bot.closeAd()
                    self.bot.botSleep(1)
        print("失败 一键收集金币")
        return False

    def collectResource(self,imgKey,name,maxTry,postDelay):
        for attempt in range(maxTry):
            pos = self.bot.findImage(self.images[imgKey],name,self.bot.conf,0.5)
            if pos:
                pyautogui.click(pos)
                print(f"收集 {name}: {attempt+1}")
            elif not pos and attempt > 0:
                print(f"完成收集 {name}")
                return True
            else:
                print(f"没有 {name}")
                return True
            self.bot.botSleep(postDelay)
        print("超出最大尝试限制")
        return False

    def run(self):
        self.bot.botSleep(2)
        pyautogui.moveTo(self.bot.wid/10*8,self.bot.hei/2)
        pyautogui.click()
        self.bot.closeAd()
        for island in self.bot.islands:
            print(f"------ 前往岛屿：{island} ------")
            self.bot.toIsland(island)
            self.bot.botSleep(2)
            print()
            print(f"------ 收取金币 ------")
            self.collectCoinFast()
            self.bot.botSleep(2)
            print(f"------ 收取钻石 ------")
            self.collectResource("diamondCollect","Diamond",1,0.5)
            self.bot.botSleep(1)
            print(f"------ 收取食物 ------")
            self.collectResource("foodCollect","Food",5,0.5)
            self.bot.botSleep(1)
