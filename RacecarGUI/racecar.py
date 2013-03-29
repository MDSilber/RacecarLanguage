#!/usr/bin/python

from Tkinter import *
import tkFileDialog

current_program = None

class Program:
	def __init__(self):
		self.name = None
		self.file_obj = None

def runProgram(code):
	if len(code) > 1:
		print code[:-1]
	else:
		print "Blank"

def openFile():
	file_name = tkFileDialog.askopenfile_name()
	file_object = open(file_name,'r+')
	current_program = Program()
	current_program.name = file_name
	current_program.file_obj = file_object
	code.delete(1.0,END)
	code.insert(1.0,file_object.read())
	print file_name

def save():
	pass
def saveFile():
	pass
def saveFileAs():
	pass

def clear():
	code.delete(1.0,END)

root = Tk()
root.title('Racecar')
root.rowconfigure('all',minsize=100)
root.columnconfigure('all',minsize=100)
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry	("%dx%d"%(window_width,window_height))

menu_bar = Menu(root)
menu = Menu(menu_bar, tearoff=0)
menu.add_command(label="Open", command = lambda: openFile())
menu.add_command(label="Save", command = lambda: save())
menu.add_separator()
menu.add_command(label="Quit", command = lambda: exit())
menu_bar.add_cascade(label="File",menu=menu)

root.config(menu=menu_bar)

#code is the window in which the code is written
code = Text(root, width=50, height = window_height/20+4)
code.grid(row=0, rowspan=1, columnspan=2)

#canvas is where the car will go
canvas_frame= Frame(root, width = window_width/1.5, height = code.winfo_height()*525)
canvas_frame.configure(borderwidth=1.5,background='black')
canvas_frame.grid(row=0,column=2)
canvas = Canvas(canvas_frame, width = window_width/1.5, height = code.winfo_height()*525)
canvas.pack()

#run_button passes code into a run program method
run_button = Button(root, text = "Run", command = lambda: runProgram(code.get(1.0,END)))
run_button.grid(row=1,column=0)

#clear_button clears the code in the text box
clear_button = Button(root, text = "Clear code", command = lambda: clear())
clear_button.grid(row=1,column=1)

#code to add widgets goes here
root.mainloop()
