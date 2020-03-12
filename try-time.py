import tkinter as tk # Python 3.x 
import time 

# function which changes time on Label 
def update_time(): 
    # change text on Label 
    lbl['text'] = time.strftime('Current time: %H:%M:%S') 

    # run `update_time` again after 1000ms (1s) 
    root.after(1000, update_time) # function name without() 


# create window 
root = tk.Tk() 

# create label for current time 
lbl = tk.Label(root, text='Current time: 00:00:00') 
lbl.pack() 

# run `update_time` first time after 1000ms (1s) 
root.after(1000, update_time) # function name without() 
#update_time() # or run first time immediately 

# "start the engine" 
root.mainloop() 