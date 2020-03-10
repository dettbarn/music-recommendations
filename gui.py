import json
import requests
import operator
import tkinter

root = tkinter.Tk()

def compute():
	exec(compile(open("musicrecs.py", "rb").read(), "musicrecs.py", 'exec'))

btn = tkinter.Button(root, text='Run', width=25, command=compute)
btn.pack()
root.mainloop()