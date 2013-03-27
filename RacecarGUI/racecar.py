#!/usr/bin/python

from Tkinter import *

def runProgram(code):
	if len(code) > 1:
		print code[:-1]
	else:
		print "Blank"

root = Tk()
root.title('Racecar')
root.rowconfigure('all',minsize=100)
root.columnconfigure('all',minsize=100)

menubar = Menu(root)
menu = Menu(menubar, tearoff=0)
menu.add_command(label="Open")
menu.add_command(label="Save")
menu.add_separator()
menu.add_command(label="Quit", command = lambda: exit())
menubar.add_cascade(label="File",menu=menu)

root.config(menu=menubar)

code = Text(root)
code.grid(row=0, rowspan=1, columnspan=1)

#button passes code into a run program method
button = Button(root, text = "Run", command = lambda: runProgram(code.get(1.0,END)))
button.grid(row=1,column=0)

#code to add widgets goes here
root.mainloop()
