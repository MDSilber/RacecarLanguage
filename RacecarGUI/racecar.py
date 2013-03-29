#!/usr/bin/python

from Tkinter import *
import tkFileDialog

currentProgram = None

class Program:
	name = ''
	def __init__(self, name = None):
		self['name'] = name

def runProgram(code):
	if len(code) > 1:
		print code[:-1]
	else:
		print "Blank"

def openFile():
	filename = tkFileDialog.askopenfilename()
	currentProgram = filename
	file = open(filename,'r+')
	code.delete(1.0,END)
	code.insert(1.0,file.read())
	print filename

def save():
	pass
def saveFile():
	pass
def saveFileAs():
	pass

root = Tk()
root.title('Racecar')
root.rowconfigure('all',minsize=100)
root.columnconfigure('all',minsize=100)

menubar = Menu(root)
menu = Menu(menubar, tearoff=0)
menu.add_command(label="Open", command = lambda: openFile())
menu.add_command(label="Save", command = lambda: save())
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
