"""
pystray: systray libary
PIL: python image library
keyboard: hotkey library
threading: threading, to alow multiple functions to run concurrently
tkinter: TK interface for menu
time: sleep function
"""

from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw
import keyboard
import threading
import tkinter as tk
from tkinter import Menu
import time

VERSION = '0.0.1'
image = Image.open('clipmac.png')
show_menu_flag = False
exit_flag = False

def menu_ver():
    return 'clipMAC v' + str(VERSION)

def action1():
    print("Action 1")

def action2():
    print("Action 2")

def about_clicked(icon, item):
    print(f'clipMAC v{VERSION}')

def quit_clicked(icon, item):
    global exit_flag
    icon.stop()
    exit_flag = True
    
def on_hotkey():
    print('Hotkey detected!')

def create_systray():
    print('running create_systray()...')
    image = Image.open('clipmac.png')
    icon_menu = menu(
        item(menu_ver(), about_clicked),
        item('Quit', quit_clicked)
    )

    tray_icon = icon('clipMAC', image, menu=icon_menu)
    tray_icon.run()

def show_menu():
    global show_menu_flag
    show_menu_flag = True

root = tk.Tk()
root.withdraw()

context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Action 1", command=action1)
context_menu.add_command(label="Action 2", command=action2)

def custom_tkinter_loop():
    global show_menu_flag, exit_flag
    while not exit_flag:
        root.update()
        if show_menu_flag:
            x, y = root.winfo_pointerxy()
            context_menu.post(x, y)
            show_menu_flag = False
        time.sleep(0.1)
    root.destroy()

    

icon_thread = threading.Thread(target=create_systray)
icon_thread.start()

keyboard.add_hotkey('ctrl+alt+shift+m', show_menu)

custom_tkinter_loop()

icon_thread.join()

