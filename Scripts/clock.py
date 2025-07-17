import tkinter as tk
import time
import threading

def updateTime():
    while True:
        try:
            clockWin.update()
            t = time.asctime()
            l.configure(text=t)
            time.sleep(0.85)
        except:
            break

def run_clock():
    global clockWin, l
    
    clockWin = tk.Tk()
    clockWin.title('Clock')

    l = tk.Label(clockWin, text = time.asctime())
    l.grid()

    threading.Thread(target = updateTime()).start()

    #clockWin.mainloop()
