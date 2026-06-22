import customtkinter as ctk
import threading
import time
import sys
import os
import config

from core.base_bot import MSMbot,ForceStop
from core.task.collect_bot import CollectBot
from core.task.bake_bot import BakeBot

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.stopEvent = threading.Event()
        self.botThread = None
        self.running = False

        self.disColor = "gray30"
        self.norColor = "#343638"

        self.protocol("WM_DELETE_WINDOW",self.closing)

        self.title("MSM Helper: 日常-填蛋-烘培 v0.4.0")
        self.geometry("500x350")
        #日常收集
        self.collectFrame = ctk.CTkFrame(self)
        self.collectFrame.pack(padx=20,pady=10,fill="x")
        self.collectBool = ctk.BooleanVar(value=False)
        self.collectCheck = ctk.CTkCheckBox(self.collectFrame,text="日常收集",variable=self.collectBool)
        self.collectCheck.pack(padx=10,pady=10,anchor="w")
        #烘培
        self.bakeFrame = ctk.CTkFrame(self)
        self.bakeFrame.pack(padx=20,pady=10,fill="x")
        self.bakeBool = ctk.BooleanVar(value=False)
        self.bakeCheck = ctk.CTkCheckBox(self.bakeFrame,text="食物烘培",variable=self.bakeBool,command=self.bakeStatu)
        self.bakeCheck.pack(padx=10,pady=10,anchor="w")

        self.bakeInFrame = ctk.CTkFrame(self.bakeFrame,fg_color="transparent")
        self.bakeInFrame.pack(padx=10,pady=10,fill="x")
        #单个烘培
        self.foodCombo = ctk.CTkComboBox(self.bakeInFrame,values=config.FOOD)
        self.foodCombo.grid(row=0,column=0,padx=5,pady=5)
        self.amountEntry = ctk.CTkEntry(self.bakeInFrame,placeholder_text="制作数量")
        self.amountEntry.grid(row=0,column=1,padx=5,pady=5)
        #一键重新烘培
        self.food2Bool = ctk.BooleanVar(value=True)
        self.food2Check = ctk.CTkCheckBox(self.bakeInFrame,text="重新烘培模式",variable=self.food2Bool,command=self.bakeStatu)
        self.food2Check.grid(row=1,column=0,padx=5,pady=10)
        self.amount2Entry = ctk.CTkEntry(self.bakeInFrame,placeholder_text="岛屿数量")
        self.amount2Entry.grid(row=1,column=1,padx=5,pady=10)

        self.startBtn = ctk.CTkButton(self,text="开始运行",command=self.startThread)
        self.startBtn.pack(pady=10)
        self.stopBtn = ctk.CTkButton(self,text="终止运行",command=self.stopThread,state="disabled")
        self.stopBtn.pack(pady=10)

        self.bakeStatu()
    #切换组件禁用状态
    def bakeStatu(self):
        bakeOn = self.bakeBool.get()
        mode2 = self.food2Bool.get()

        if not bakeOn:
            self.foodCombo.configure(state="disabled",fg_color=self.disColor)
            self.amountEntry.configure(state="disabled",fg_color=self.disColor)
            self.food2Check.configure(state="disabled")
            self.amount2Entry.configure(state="disabled",fg_color=self.disColor)
        elif mode2:
            self.foodCombo.configure(state="disabled",fg_color=self.disColor)
            self.amountEntry.configure(state="disabled",fg_color=self.disColor)
            self.food2Check.configure(state="normal")
            self.amount2Entry.configure(state="normal",fg_color=self.norColor)
        else:
            self.foodCombo.configure(state="normal",fg_color=self.norColor)
            self.amountEntry.configure(state="normal",fg_color=self.norColor)
            self.food2Check.configure(state="normal")
            self.amount2Entry.configure(state="disabled",fg_color=self.disColor)
    #程序延迟关闭写日志
    def closing(self):
        print("程序关闭中")
        if sys.stdout != sys.__stdout__:
            sys.stdout.flush()
            sys.stdout.close()
            sys.stdout = sys.__stdout__
        self.destroy()
        os._exit(0)

    def startThread(self):
        if self.running:
            return
        self.startBtn.configure(text="运行中",state="disabled")
        self.stopBtn.configure(state="normal")
        self.running = True

        self.stopEvent.clear()

        self.taskConfig = {
            "collect" : self.collectBool.get(),
            "bake" : self.bakeBool.get(),
            "foodMode2" : self.food2Bool.get(),
            "foodName" : self.foodCombo.get(),
            "bakeAmount" : self.amountEntry.get(),
            "islandAmount" : self.amount2Entry.get()
        }

        self.botThread = threading.Thread(target=self.runBot,args=(self.taskConfig,),daemon=True)
        self.botThread.start()

    def stopThread(self):
        if not self.running:
            return
        self.startBtn.configure(text="开始运行",state="normal")
        self.stopBtn.configure(state="disabled")
        self.running = False

        self.stopEvent.set()

    def runBot(self,config):
        try:
            print("运行 MSMbot")
            bot = MSMbot(self.stopEvent)

            if config["collect"]:
                collectTask = CollectBot(bot)
                collectTask.run()
            if config["bake"]:
                bakeTask = BakeBot(bot)
                if config["foodMode2"]:
                    if not config["islandAmount"]:
                        print("未输入岛屿数量")
                        return
                    bakeTask.run2(int(config["islandAmount"]))
                else:
                    if not config["bakeAmount"]:
                        print("未输入制作数量")
                        return
                    bakeTask.run1(config["foodName"],int(config["bakeAmount"]))
        except ForceStop:
            pass
        except Exception as e:
            print(f"程序异常：{e}")
        finally:
            print("结束 MSMbot")
            self.after(0,self.botFinish)

    def botFinish(self):
        self.startBtn.configure(text="开始运行",state="normal")
        self.stopBtn.configure(state="disabled")
        self.running = False