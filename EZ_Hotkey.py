import threading
import tkinter
from tkinter import *
import ctypes
import keyboard
from PIL import ImageTk, Image

window = Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)

##### Prevent Alt+F4
AltF4 = False

def do_exit():
    global AltF4
    if AltF4:
        pressed_f4 = False
    else:
        close()

def alt_f4(event):
    global AltF4
    print('Alt+F4 attempt made')
    AltF4 = True

def close(*event):
    window.destroy()

window.bind('<Alt-F4>', alt_f4)
window.protocol("WM_DELETE_WINDOW", do_exit)
###########

window.title('')
window.iconbitmap(default='resources/transparent.ico')

window.geometry("848x480")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 480,
    width = 848,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"resources/background.png")
background = canvas.create_image(
    399.0, 473.5,
    image = background_img)

###########window.focus() upon clicking background
def key(event):
    print("pressed", repr(event.char))

def callback(event):
    print("Clicked at", event.x, event.y)
    window.focus()
    print("Unfocused")
canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)
canvas.pack()

#Entry1
entry1_img = PhotoImage(file = f"resources/img_textBox.png")
entry1_bg = canvas.create_image(
    612.5, 217.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1 = tkinter.Entry(window, font=('Century 26'), width=50, bd=0, highlightthickness=0)

entry1.place(
    x = 525.0, y = 185,
    width = 175.0,
    height = 65)

#Entry0
entry0_img = PhotoImage(file=f"resources/img_textBox.png")
entry0_bg = canvas.create_image(
    269.5, 217.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry0 = tkinter.Entry(window, font=('Century 26'), width=50, bd=0, highlightthickness=0)

entry0.place(
    x = 182.0, y = 185,
    width = 175.0,
    height = 65)

#Establish globals
e1 = 'undef'
e0 = 'undef'

#Listen for inputs
def gete1():
    global e1, AltF4
    e1 = 'undef'
    entry1.delete(0, END)
    print(e1)
    print('Listening for output')
    e1 = keyboard.record(until='esc')
    e1 = e1[:-1]
    print(e1)
    entry1.delete(0, END)
    entry1.insert(END, e1)
    AltF4 = False
    window.focus()

def gete0():
    global e0, AltF4
    e0 = 'undef'
    entry0.delete(0, END)
    print('Listening for input')
    e0 = keyboard.read_hotkey()
    print(e0)
    entry0.delete(0, END)
    entry0.insert(END, ('[{}]').format(e0))
    AltF4 = False
    window.focus()
    keyboard.play(e1)

def input0():
    threading.Thread(target=gete0, daemon=True).start()

def input1():
    threading.Thread(target=gete1, daemon=True).start()

#Check for focus in
def callback_entry1_focus(event):
    global e1
    e1 = 'undef'
    print('entry1 focus in')
    input1()

def callback_entry0_focus(event):
    global e0
    e0 = 'undef'
    print('entry0 focus in')
    input0()

entry0.bind("<FocusIn>", callback_entry0_focus)
entry1.bind("<FocusIn>", callback_entry1_focus)

#Play hotkey
def playe1():
    global e1
    print('awating hotkey input')
    keyboard.play(e1, speed_factor=0)

#Assing this function to loop listen for the assigned hotkey input and then play the output
def backend():
    global e1, e0
    print('\nInput: {} \nOutput: {}\n'.format(e0, e1))
    keyboard.add_hotkey(e0, playe1, suppress=True, trigger_on_release=False)

#Restart App
def restart():
    global entry1, entry0, AltF4
    window.focus()
    AltF4 = False
    keyboard.clear_all_hotkeys()
    entry0.delete(0, END)
    entry1.delete(0, END)

########## Play/End Buttton change image and backend
is_off = 'undef'
def switch():
    global is_off
    # Determine is on or off
    if is_off:
        on_button.config(image = off)
        is_off = False
        backend()

    else:
        on_button.config(image = on)
        is_off = True
        print('off')
        restart()

on = PhotoImage(file = "resources/play.png")
off = PhotoImage(file = "resources/stop.png")

########## Play/End Button basics
on_button = Button(
	image = on,
    borderwidth = 0,
    highlightthickness = 0,
    bg = "#ffffff",
    command = switch,
    relief = "flat",
    cursor="hand2")

on_button.place(
    x = 406, y = 273,
    width = 85,
    height = 85)

########## Info Button change image and backend
def info_screen():
    global infoBox
    infoBox = 'undef'
    infoBox = ImageTk.PhotoImage(Image.open("resources/infoBox.png"))
    infoScreen = Label(image=infoBox, borderwidth=0, bg="#ffffff")
    infoScreen.pack()
    infoScreen.place(x=470, y=40)
    print('info screen displayed')

def remove_screen():
    global infoBox
    infoBox = 'undef'
    infoBox = ImageTk.PhotoImage(Image.open("resources/transparent.ico"))
    infoScreen = Label(image=infoBox, borderwidth=0, bg="#ffffff")
    infoScreen.pack()
    infoScreen.place(x=470, y=40)
    print('info screen displayed')

info_is_on = 'undef'
def infoSwitch():
    global info_is_on
    if info_is_on:
        info_button.config(image = info_on)
        info_is_on = False
        info_screen()
    else:
        info_button.config(image = info_off)
        info_is_on = True
        remove_screen()
        print('info gone :(')

info_off = PhotoImage(file = "resources/info_off.png")
info_on = PhotoImage(file = "resources/info_on.png")

########## Info Button basics
info_button = Button(
    image = info_off,
    borderwidth = 0,
    highlightthickness = 0,
    bg='#ffffff',
    command = infoSwitch,
    relief = "flat",
    cursor="hand2")

info_button.place(
    x=778, y=15,
    width=40, height=40)

window.resizable(False, False)
window.mainloop()