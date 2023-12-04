"""
pystray: systray libary
PIL: python image library
keyboard: hotkey library
threading: threading, to alow multiple functions to run concurrently
tkinter: TK interface for menu
"""

from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw
import keyboard
import threading
import tkinter as tk
from tkinter import simpledialog

VERSION = '0.0.1'
image = Image.open('clipmac.png')

def menu_ver():
    return 'clipMAC v' + str(VERSION)

def action1():
    print("Action 1")

def action2():
    print("Action 2")

def about_clicked(icon, item):
    print(f'clipMAC v{VERSION}')

def quit_clicked(icon, item):
    icon.stop()
    
def on_hotkey():
    print('Hotkey detected!')

def create_systray():
    print('running create_systray()...')
    image = Image.open('clipmac.png')
#    icon_menu = icon('clipMAC', image, menu=menu(
#        item('clipMAC by Jeremy Drahos', lambda icon, item: about_clicked(icon, item)),
#        item(
#            'Quit',
#            lambda icon, item: quit_clicked(icon, item)
#        )
    icon_menu = menu(
        item(menu_ver(), about_clicked),
        item('Quit', quit_clicked)
    )

    tray_icon = icon('clipMAC', image, menu=icon_menu)
    tray_icon.run()


def show_menu():
    print('running show_menu()...')
    root = tk.Tk()
    root.withdraw()
    response = simpledialog.askstring('Menu', 'Action 1, Action 2')
    if response == '1':
        print('Action 1 detected.')
    if response == '2':
        print('Action 2 detected.')
    root.destroy()

#create_systray()

print('threading out the icon...')
icon_thread = threading.Thread(target=create_systray)
icon_thread.start()
print('done threading...')

print('listening for the hotkey...')
keyboard.add_hotkey('ctrl+alt+shift+m', show_menu())
print('through that...')

#icon.run()
