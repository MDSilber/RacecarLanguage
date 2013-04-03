#!/usr/bin/python

from Tkinter import *
from PIL import Image, ImageTk
import tkFileDialog, tkMessageBox, re, time, parser

#current_program ised used to store the current file open in order to save back
#to that file
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
    FORWARDS=1
    BACKWARDS=-1

    def __init__(self):
        self.x = 1
        self.y = 0
    
    #Note that the commented degrees are before the turn, rather than after
    def turn_right(self):
        #In this case, y can never equal zero
        if self.x == 0:
            #90 degrees
            if self.y == 1:
                self.x = 1
            #270 degrees
            else:
                self.x = -1
        #In this case, x can never equal zero
        elif self.y == 0:
            #0 degrees
            if self.x == 1:
                self.y = -1
            #180 degrees
            else:
                self.y = 1
        else:
            #45 degrees or 225 degrees
            if (self.x == 1 and self.y == 1) or (self.x == -1 and self.y == -1):
                self.y = 0
            #135 degrees or 315 degrees
            else:
                self.x = 0

    
    def turn_left(self):
        #In this case, y can never equal zero
        if self.x == 0:
            #90 degrees
            if self.y == 1:
                self.x = -1
            #270 degrees
            else:
                self.x = 1
        #In this case, x can never equal zero
        elif self.y == 0:
            #0 degrees
            if self.x == 1:
                self.y = 1
            #180 degrees
            else:
                self.y = -1
        else:
            #45 degrees or 225 degrees
            if (self.x == 1 and self.y == 1) or (self.x == -1 and self.y == -1):
                self.y = 0
            #135 degrees or 315 degrees
            else:
                self.x = 0

class Car:
    def __init__(self):
        self.position_x = 0
        self.position_y = 0
        self.wheel_direction = WheelDirection.STRAIGHT
        #Car direction starts facing right
        self.car_direction = CarDirection()
        self.image = None
        self.image_tk = None
        self.car_object = None
    
    #Drive method that updates the car's position (in the model, not on the UI)
    #UI animation will need to be done moving x and y simultaneously
    def drive(self, steps):
        if self.wheel_direction == WheelDirection.STRAIGHT:
            self.position_x += self.car_direction.x * steps
            self.position_y += self.car_direction.y * steps
        elif self.wheel_direction == WheelDirection.RIGHT:
            for _ in range(steps):
                self.car_direction.turn_right()
        else:
            for _ in range(steps):
                self.car_direction.turn_left()
    
    #Decided on a 10:1 pixels to steps ratio

def steps_to_pixels(steps):
    return 10*steps

#API Functions
#direction must be either CarDirection.FORWARDS or CarDirection.BACKWARDS
def translate_car(steps, direction):
    global car
        
    if car.wheel_direction == WheelDirection.STRAIGHT:
        for _ in range(0,steps_to_pixels(int(steps))):
            time.sleep(0.025)
            #car_direction is FORWARDS or BACKWARDS (1 and -1 respectively)
            canvas.move(car.car_object,direction*car.car_direction.x,direction*car.car_direction.y)
            car.drive(steps)
            canvas.update()
    else:
        #rotate car
        rotate_car(steps, car.wheel_direction)

#Demo movement
def demo(steps):
    
    #Move right
    for _ in range(0,10*int(steps)):
        time.sleep(0.025)
        canvas.move(car.car_object, car.car_direction.x, car.car_direction.y)
        canvas.update()
    #Rotate counterclockwise
    for i in range(0,45):
        time.sleep(0.025)
        canvas.delete(car.car_object)
        car.image_tk = ImageTk.PhotoImage(car.image.rotate(i+1))
        car.car_object = canvas.create_image(30+10*int(steps),250, image=car.image_tk)
        car.car_direction.y = -1
        canvas.update()
    #Move diagonal
    for _ in range(0,10*int(steps)):
        time.sleep(0.025)
        canvas.move(car.car_object,car.car_direction.x,car.car_direction.y)
        canvas.update()
    #Rotate clockwise
    for i in range(0,45):
        time.sleep(0.025)
        canvas.delete(car.car_object)
        car.image_tk = ImageTk.PhotoImage(car.image.rotate(44-i))
        car.car_object = canvas.create_image(30+20*int(steps),250-10*int(steps), image=car.image_tk)
        car.car_direction.y = 0
        canvas.update()
    #Move right
    for _ in range(0,10*int(steps)):
        time.sleep(0.025)
        canvas.move(car.car_object,car.car_direction.x,car.car_direction.y)
        canvas.update()

#direction must be WheelDirection.LEFT, WheelDirection.RIGHT, or WheelDirection.STRAIGHT
def steer_wheels(direction):
    global car
    car.wheel_direction = direction
    pass

def rotate_car(steps, direction):
        global car
        
        for i in range(0,int(steps)):
                time.sleep(0.025)
                canvas.delete(car.car_object)
                
                if direction == WheelDirection.LEFT:
                        car.image_tk = ImageTk.PhotoImage(car.image.rotate(i+1))
                        car.car_direction.turn_left()
                elif direction == WheelDirection.RIGHT:
                        car.image_tk = ImageTk.PhotoImage(car.image.rotate(i-1))
                        car.car_direction.turn_right()
                else:
                        return

                car.car_object = canvas.create_image(car.position_x, car.position_y, image=car.image_tk)
                canvas.update()

def print_to_console(message):
    #Should console be cleared each time the program is restart? Or should there
    #be a button?
    console.insert(message+'\n')

#Menu functions
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

def clear_console():
    if console.get(1.0,END) == '':
        return
    else:
        console.delete(1.0,END)

#Code generation and compilation
#Runs code
def generate_program(code):
    if len(code) > 1:
        print code[:-1]
        demo(code)
    else:
        print "Blank"

#Checks if program is a valid Racecar program
def verify_program(code):
    pass

#car object
car = Car()

#User interface
root = Tk()
root.title('Racecar')
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry    ("%dx%d"%(window_width-100,window_height-100))

menu_bar = Menu(root)

menu = Menu(menu_bar, tearoff=0)
menu.add_command(label="Open", command = open_file)
menu.add_command(label="Save", command = save)
menu.add_command(label="Save As", command= save_file_as)
menu.add_separator()
menu.add_command(label="Quit", command = exit)
menu_bar.add_cascade(label="File",menu=menu)

menu = Menu(menu_bar, tearoff=0)
menu.add_command(label="Verify Code", command= lambda: verify_program(code.get(1.0,END)))
menu.add_command(label="Run Code", command = lambda: generate_program(code.get(1.0,END)))
menu.add_command(label="Clear Code", command = clear)
menu.add_command(label="Clear Console", command = clear_console)
menu_bar.add_cascade(label="Code",menu=menu)

root.config(menu=menu_bar)

#frame for left side of window
left_frame = Frame(root)

#label for code window
code_label = Label(left_frame, text="Enter code here", anchor=W,pady=5)

#frame for code window to hold textbox and scrollbar
code_frame = Frame(left_frame)

#scrollbar for code window
code_scrollbar = Scrollbar(code_frame)
code_scrollbar.pack(side=RIGHT, fill=Y)

#code is the window in which the code is written
code = Text(code_frame, width=50, height = 42, wrap=WORD, yscrollcommand=code_scrollbar.set)

#run_button passes code into a run program method
run_button = Button(left_frame, text = "Run Code", pady=5, padx=5, command = lambda: generate_program(code.get(1.0,END)))

#clear_button clears the code in the text box
clear_button = Button(left_frame, text = "Clear Code", command = clear)

#canvas is where the car will go
canvas_frame= Frame(root, width = window_width/1.5, height = window_height-300,padx=2,pady=2)
canvas_frame.configure(borderwidth=1.5,background='black')
canvas = Canvas(canvas_frame, width = window_width/1.5, height = window_height-300)
car.image = Image.open('images/car.png')
car.image_tk = ImageTk.PhotoImage(car.image)
car.car_object = canvas.create_image(30,250,image=car.image_tk)

#label above the console
console_label = Label(root, text = "Console", anchor=W,pady=5)

#frame for the console to hold the textbox and the scrollbar
console_frame = Frame(root)

#scrollbar for the console
console_scrollbar = Scrollbar(console_frame)
console_scrollbar.pack(side=RIGHT,fill=Y)

#console to print to
console = Text(console_frame, width = int(window_width/1.5), height = 10,
                                        padx=2, pady=2, wrap=WORD, yscrollcommand=console_scrollbar.set)
console.config(state=DISABLED)

#add them to GUI Window
#These are grouped logically in order to better see what's going on
left_frame.pack(side=LEFT)

code_label.pack()

code_frame.pack()
code.pack()

run_button.pack(side=LEFT)
clear_button.pack(side=RIGHT)

canvas_frame.pack()
canvas.pack()

console_label.pack()

console_frame.pack()
console.pack()

code_scrollbar.config(command=code.yview)
console_scrollbar.config(command=console.yview)

root.mainloop()
