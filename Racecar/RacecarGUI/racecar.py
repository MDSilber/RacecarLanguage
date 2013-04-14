#!/usr/bin/python

from Tkinter import *
from PIL import Image, ImageTk
import tkFileDialog, tkMessageBox, re, time, Racecar.Tree, Racecar.Compiler

#current_program ised used to store the current file open in order to save back
#to that file
current_program = None

class Program:
    def __init__(self):
        self.name = ''
        self.file_obj = None

#Static variables for turning the car
class WheelDirection:
  LEFT=1
  RIGHT=-1

#Car direction object
#X and Y can be 1,0,-1 respectively. The only invalid combination is when x = 0
#and y = 0. Positive axes point right and up respectively

class CarDirection:
    FORWARDS=1
    BACKWARDS=-1
    
    def __init__(self):
        self.direction = 0
    
    DIRECTIONS = [(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1)]

    def get_direction(self):
        return CarDirection.DIRECTIONS[self.direction]

    def turn_right(self):
        self.direction = (self.direction - 1) % len(CarDirection.DIRECTIONS)

    def turn_left(self):
        self.direction = (self.direction + 1) % len(CarDirection.DIRECTIONS)


class Car:
    def __init__(self):
        self.position_x = 0
        self.position_y = 0
        #Car direction starts facing right
        self.car_direction = CarDirection()
        self.image = None
        self.image_tk = None
        self.car_object = None
    
    #Drive method that updates the car's position (in the model, not on the UI)
    #UI animation will need to be done moving x and y simultaneously
    def update_position(self, steps):
        self.position_x += self.car_direction.get_direction()[0] * steps
        self.position_y += self.car_direction.get_direction()[1] * steps
    
    #Decided on a 10:1 pixels to steps ratio

def steps_to_pixels(steps):
    return 10*steps

#API Functions
#direction must be either CarDirection.FORWARDS or CarDirection.BACKWARDS
def translate_car(steps, direction):
    global car
    steps = int(steps)
    direction = int(direction)
    
    for _ in range(0,steps_to_pixels(int(steps))):
        time.sleep(0.025)
        #car_direction is FORWARDS or BACKWARDS (1 and -1 respectively)
        canvas.move(car.car_object, direction * car.car_direction.get_direction()[0], direction * car.car_direction.get_direction()[1])
        canvas.update()

    car.update_position(steps_to_pixels(steps))

#Demo movement
def demo(steps):

    #translate_car(steps, CarDirection.FORWARDS)
    #rotate_car(WheelDirection.LEFT)
    #translate_car(steps, CarDirection.FORWARDS)
    #rotate_car(WheelDirection.RIGHT)
    #translate_car(steps, CarDirection.FORWARDS)
    print_to_console(str(car.position_x) + ", " + str(car.position_y))

#direction must be WheelDirection.LEFT or WheelDirection.RIGHT
def rotate_car(direction):
        global car
        
        #This is current index in DIRECTIONS array
        current_direction_deg = car.car_direction.direction*45

        if direction == WheelDirection.LEFT:
          car.car_direction.turn_left()
        elif direction == WheelDirection.RIGHT:
          car.car_direction.turn_right()
        else:
          return
        

        for i in range(0,45):
                time.sleep(0.025)
                canvas.delete(car.car_object)
                
                if direction == WheelDirection.LEFT:
                        car.image_tk = ImageTk.PhotoImage(car.image.rotate(current_direction_deg + i))
                elif direction == WheelDirection.RIGHT:
                        car.image_tk = ImageTk.PhotoImage(car.image.rotate(current_direction_deg - i))
                else:
                        return

                car.car_object = canvas.create_image(car.position_x, car.position_y, image=car.image_tk)
                canvas.update()

def print_to_console(message):
    
    #Should console be cleared each time the program is restart? Or should there
    #be a button?
    console.config(state=NORMAL)
    console.insert(END, str(message) + '\n')
    console.config(state=DISABLED)

#Course generation functions
def course_one():
    pass

def course_two():
    pass

def course_three():
    pass

def course_four():
    pass

def course_five():
    pass

def clear_course():
    pass

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

def save():
    global current_program
    if current_program == None:
        save_file_as()
    else:
        save_file()

def save_file():
    global current_program
    if not current_program.file_obj.closed:
        current_program.file_obj.close()
    #Open file for writing (will clear it)    
    current_program.file_obj = open(current_program.name, 'w')
    current_program.file_obj.truncate()
    current_program.file_obj.write(code.get(1.0,END))
    current_program.file_obj.close()

def save_file_as():
    global current_program
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
        #print code[:-1]
        #demo(code)
        exec(Racecar.Compiler.getPythonCode(code), globals())
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

menu = Menu(menu_bar, tearoff=0)
menu.add_command(label="Course 1", command = course_one)
menu.add_command(label="Course 2", command = course_two)
menu.add_command(label="Course 3", command = course_three)
menu.add_command(label="Course 4", command = course_four)
menu.add_command(label="Course 5", command = course_five)
menu.add_separator()
menu.add_command(label="Clear course", command = clear_course)
menu_bar.add_cascade(label="Courses", menu=menu)

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
code = Text(code_frame, width=50, height = 30, wrap=WORD, yscrollcommand=code_scrollbar.set)

#run_button passes code into a run program method
run_button = Button(left_frame, text = "Run Code", pady=5, padx=5, command = lambda: generate_program(code.get(1.0,END)))

#clear_button clears the code in the text box
clear_button = Button(left_frame, text = "Clear Code", command = clear)

#canvas is where the car will go
canvas_frame= Frame(root, width = window_width/1.5, height = window_height-300,padx=2,pady=2)
canvas_frame.configure(borderwidth=1.5,background='black')
canvas = Canvas(canvas_frame, width = window_width/1.5, height = window_height-300)
car.image = Image.open('Racecar/RacecarGUI/images/racecar.png')
car.image_tk = ImageTk.PhotoImage(car.image)
car.car_object = canvas.create_image(30,250,image=car.image_tk)
car.position_x = 30
car.position_y = 250

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
left_frame.pack(side=LEFT,fill=BOTH)

code_label.pack()

code_frame.pack(fill=BOTH)
code.pack(fill=BOTH)

run_button.pack(side=LEFT)
clear_button.pack(side=RIGHT)

canvas_frame.pack(fill=BOTH)
canvas.pack(fill=BOTH)

console_label.pack()

console_frame.pack(fill=BOTH)
console.pack(fill=BOTH)

code_scrollbar.config(command=code.yview)
console_scrollbar.config(command=console.yview)

root.mainloop()
