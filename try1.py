import tkinter as tk
from tkinter import ttk
import time
#https://blog.csdn.net/seeker3/article/details/103830681
win=tk.Tk()

#progressbarVar=tk.IntVar()

progress_bar=ttk.Progressbar(win, orient='horizontal', length=286, mode='determinate') ##

#progress_bar=ttk.Progressbar(win, orient='horizontal', length=286, mode='determinate', variable=progressbarVar)

progress_bar.grid(column=0, row=0, padx=5, pady=5)

progress_bar['maximum']=100
for i in range(101):
    progress_bar['value']=i ##
    #progressbarVar.set(i)
    progress_bar.update()
    time.sleep(0.05)

win.mainloop()
