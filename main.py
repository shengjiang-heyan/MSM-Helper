import sys

from gui.app_window import AppWindow

def main():
    logPath = "gameLog.txt"
    sys.stdout = open(logPath,"a",encoding="utf-8",buffering=1)

    app = AppWindow()
    app.mainloop()

if __name__ == "__main__":
    main()