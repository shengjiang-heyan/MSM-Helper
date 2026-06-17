import customtkinter as ctk
import threading
import time
import sys
import os

from core.MSM_bot import MSMbot

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW",self.closing)

        self.title("MSM Helper: 日常-填蛋-烘培 v0.3.0")
        self.geometry("500x300")
        self.label = ctk.CTkLabel(self,text="设置")
        self.label.pack(padx=15,pady=15,fill="both")

        self.startBtn = ctk.CTkButton(self,text="开始运行",command=self.startThread)
        self.startBtn.pack(pady=50)

        self.running = False

    def closing(self):
        print("程序关闭中")
        if sys.stdout != sys.__stdout__:
            print("程序被强行关闭")
            sys.stdout.flush()
            sys.stdout.close()
            sys.stdout = sys.__stdout__
        self.destroy()
        os._exit(0)

    def startThread(self):
        if self.running:
            return
        self.running = True
        self.startBtn.configure(text="运行中",state="disabled")

        botThread = threading.Thread(target=self.runBot,daemon=True)
        botThread.start()

    def runBot(self):
        try:
            print("运行 MSMbot")
            bot = MSMbot()
            bot.run()
        finally:
            self.running = False
            print("结束 MSMbot")