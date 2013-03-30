#!/usr/bin/python

from Tkinter import *
import tkFileDialog, tkMessageBox, re, time
from PIL import Image, ImageTk

current_program = None

class Program:
	def __init__(self):
		self.name = ''
		self.file_obj = None

class WheelDirection:
	STRAIGHT=0
	LEFT=1
	RIGHT=2

#Car direction object
#X and Y can be 1,0,-1 respectively. The only invalid combination is when x = 0
#and y = 0. Positive axes point right and up respectively
class CarDirection:
	def __init__(self):
		self.x = 1
		self.y = 0
	
	#Note that the commented degrees are before the turn, rather than after
	def turn_right(self):
		#In this case, y can never equal zero
		if x == 0:
			#90 degrees
			if y == 1:
				x = 1
			#270 degrees
			else:
				x = -1
		#In this case, x can never equal zero
		elif y == 0:
			#0 degrees
			if x == 1:
				y = -1
			#180 degrees
			else:
				y = 1
		else:
			#45 degrees or 225 degrees
			if (x == 1 and y == 1) or (x == -1 and y == -1):
				y = 0
			#135 degrees or 315 degrees
			else:
				x = 0

	
	def turn_left(self):
		#In this case, y can never equal zero
		if x == 0:
			#90 degrees
			if y == 1:
				x = -1
			#270 degrees
			else:
				x = 1
		#In this case, x can never equal zero
		elif y == 0:
			#0 degrees
			if x == 1:
				y = 1
			#180 degrees
			else:
				y = -1
		else:
			#45 degrees or 225 degrees
			if (x == 1 and y == 1) or (x == -1 and y == -1):
				y = 0
			#135 degrees or 315 degrees
			else:
				x = 0

class Car:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.wheel_direction = WheelDirection.STRAIGHT
		#Car direction starts facing right
		self.car_direction = CarDirection()
		self.car_object = None
	
	#Drive method that updates the car's position (in the model, not on the UI)
	#UI animation will need to be done moving x and y simultaneously
	def drive(steps):
		if self.wheel_direction == WheelDirection.STRAIGHT:
			self.x += self.car_direction.x * steps
			self.y += self.car_direction.y * steps
		elif self.wheel_direction == WheelDirection.RIGHT:
			for _ in range(steps):
				self.turn_right()
		else:
			for _ in range(steps):
				self.turn_left()
	
	def turn_right():
		self.car_direction.turn_right()

	def turn_left():
		self.car_direction.turn_left()
		
	#Decided on a 10:1 pixels to steps ratio
	def steps_to_pixels(steps):
		return 10*steps

#UI methods
def generate_program(code):
	if len(code) > 1:
		print code[:-1]
		move_car(code)
	else:
		print "Blank"

def move_car(steps):
	global car
	car_coords = canvas.coords(car.car_object)
	for i in range(0,10*int(steps)):
		time.sleep(0.025)
		canvas.move(car.car_object,1,0)
		canvas.update()
	for i in range(0,10*int(steps)):
		time.sleep(0.025)
		canvas.move(car.car_object,0,1)
		canvas.update()

def open_file():
	global current_program
	
	#Keep returning to the file dialog if they didn't select a .race file
	while True:
		file_name = tkFileDialog.askopenfilename(defaultextension=".race")
		if file_name == '':
			return

		#Check validity of file being opened
		file_regex = re.compile("\w*\.race$")
		if len(file_regex.findall(file_name)) == 0:
			tkMessageBox.showwarning("Open File Error",
																			"You must open a .race file")
		else:
			break
	
	file_object = open(file_name,'r')
	current_program = Program()
	current_program.name = file_name
	current_program.file_obj = file_object
	code.delete(1.0,END)
	code.insert(1.0,file_object.read())
	current_program.file_obj.close()
	print file_name
	print current_program.name

def save():
	global current_program
	print "Save"
	if current_program == None:
		save_file_as()
	else:
		save_file()

def save_file():
	global current_program
	print "Save file"
	if not current_program.file_obj.closed:
		current_program.file_obj.close()
	#Open file for writing (will clear it)	
	current_program.file_obj = open(current_program.name, 'w')
	current_program.file_obj.truncate()
	current_program.file_obj.write(code.get(1.0,END))
	current_program.file_obj.close()

def save_file_as():
	global current_program
	print "Save file as"
	file_name = tkFileDialog.asksaveasfilename(defaultextension=".race")
	
	#Defaults to saving on the desktop
	if file_name == '':
		file_name = '~/Desktop/racecar_program.race'
	
	current_program = Program()
	current_program.name = file_name
	current_program.file_obj = open(file_name, 'w')
	current_program.file_obj.write(code.get(1.0,END))
	current_program.file_obj.close()

def clear():
	if code.get(1.0,END) == '':
		return
	
	if tkMessageBox.askyesno("Clear code", 
							"Are you sure you want to delete all of your code?"):
		code.delete(1.0,END)

#User interface
root = Tk()
root.title('Racecar')
root.rowconfigure('all',minsize=100)
root.columnconfigure('all',minsize=100)
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry	("%dx%d"%(window_width,window_height))

menu_bar = Menu(root)
menu = Menu(menu_bar, tearoff=0)
menu.add_command(label="Open", command = lambda: open_file())
menu.add_command(label="Save", command = lambda: save())
menu.add_separator()
menu.add_command(label="Quit", command = lambda: exit())
menu_bar.add_cascade(label="File",menu=menu)

root.config(menu=menu_bar)

#code is the window in which the code is written
code = Text(root, width=50, height = window_height/20+4)
code.grid(row=0, rowspan=1, columnspan=2)

#car object
car = Car()

#canvas is where the car will go
canvas_frame= Frame(root, width = window_width/1.5, height = code.winfo_height()*525)
canvas_frame.configure(borderwidth=1.5,background='black')
canvas_frame.grid(row=0,column=2)
canvas = Canvas(canvas_frame, width = window_width/1.5, height = code.winfo_height()*525)
car_image = PhotoImage(file='car.GIF')
car.car_object = canvas.create_image(30,250,image=car_image)
canvas.pack()

#run_button passes code into a run program method
run_button = Button(root, text = "Run", command = lambda: generate_program(code.get(1.0,END)))
run_button.grid(row=1,column=0)

#clear_button clears the code in the text box
clear_button = Button(root, text = "Clear code", command = lambda: clear())
clear_button.grid(row=1,column=1)

#code to add widgets goes here
root.mainloop()
