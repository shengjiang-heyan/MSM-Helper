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

        self.stopEvent = threading.Event()
        self.botThread = None

        self.protocol("WM_DELETE_WINDOW",self.closing)

        self.title("MSM Helper: 日常-填蛋-烘培 v0.3.0")
        self.geometry("500x300")
        self.label = ctk.CTkLabel(self,text="设置")
        self.label.pack(padx=15,pady=15,fill="both")

        self.startBtn = ctk.CTkButton(self,text="开始运行",command=self.startThread)
        self.stopBtn = ctk.CTkButton(self,text="终止运行",command=self.stopThread,state="disabled")
        self.startBtn.pack(pady=10)
        self.stopBtn.pack(pady=20)

        self.running = False

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
        self.botThread = threading.Thread(target=self.runBot,daemon=True)
        self.botThread.start()

    def stopThread(self):
        if not self.running:
            return
        self.startBtn.configure(text="开始运行",state="normal")
        self.stopBtn.configure(state="disabled")
        self.running = False

        self.stopEvent.set()

    def runBot(self):
        try:
            print("运行 MSMbot")
            bot = MSMbot(self.stopEvent)
            bot.run()
        finally:
            self.startBtn.configure(text="开始运行",state="normal")
            self.stopBtn.configure(state="disabled")
            self.running = False

            print("结束 MSMbot")