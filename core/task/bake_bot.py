import pyautogui
import config

from core.base_bot import MSMbot

class BakeBot:
    def __init__(self,bot:MSMbot):
        self.bot = bot
        self.conf = 0.9

        self.images = {
            "oven" : config.getImage("Oven.png"),
            "bake" : config.getImage("Bake.png"),
            "confirm" : config.getImage("Confirm.png"),
            "reBake" : config.getImage("ReBake.png")
        }

    def bake(self):
        pos = self.bot.findImage(self.images["oven"],"Oven",self.conf,2)
        if not pos:
            return False
        pyautogui.click(pos)
        self.bot.botSleep(1)
        pos = self.bot.findImage(self.images["bake"],"Bake",self.conf,10)
        if pos:
            pyautogui.click(pos)
            self.bot.botSleep(1)
            for reTry in range(5):
                pos = self.bot.findImage(config.getImage(f"Food/{self.food}.png"),self.food,self.conf,10)
                if pos:
                    pyautogui.click(pos)
                    self.bot.botSleep(1)
                    pos = self.bot.findImage(self.images["confirm"],"Confirm",self.conf,10)
                    if pos:
                        pyautogui.click(pos)
                        self.bot.botSleep(1)
                        pyautogui.moveTo(self.bot.wid/10*8,self.bot.hei/2)
                        pyautogui.click()
                        self.amount -= 1
                    break
                else:
                    pyautogui.scroll(-100)
        return True

    def reBake(self):
        pos = self.bot.findImage(self.images["oven"],"Oven",self.conf,10)
        if pos:
            pyautogui.click(pos)
            self.bot.botSleep(1)
            pos = self.bot.findImage(self.images["reBake"],"reBake",self.conf,10)
            if pos:
                pyautogui.click(pos)
                self.bot.botSleep(1)
                pos = self.bot.findImage(self.images["confirm"],"Confirm",self.conf,10)
                if pos:
                    pyautogui.click(pos)
                    self.bot.botSleep(1)
                    pyautogui.moveTo(self.bot.wid/10*8,self.bot.hei/2)
                    pyautogui.click()

    def run1(self,food,amount):
        self.food = food
        self.amount = amount

        for island in self.bot.islands:
            if not self.amount:
                break
            self.bot.toIsland(island)
            self.bot.botSleep(2)
            while self.amount:
                if not self.bake():
                    break
                self.bot.botSleep(1)

    def run2(self,amount):
        for islandNum in range(amount):
            island = self.bot.islands[islandNum]
            self.bot.toIsland(island)

            self.reBake()
