"""
pystray: systray libary
PIL: python image library
keyboard: hotkey library
threading: threading, to alow multiple functions to run concurrently
tkinter: TK interface for menu
time: sleep function
webbrowser: open url in default browser for vendor lookup
win32clipboard: get clipboard data
"""

from tkinter import Menu
import threading
import tkinter as tk
import time
import webbrowser
import keyboard
import win32clipboard
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image

VERSION = '0.0.1'
RAWMAC = ''
image = Image.open('clipmac.png')
show_menu_flag = False
exit_flag = False
strip_chars = ":-."

def menu_ver():
    return 'clipMAC v' + str(VERSION)

def action1():
    print("Action 1")

def action2():
    print("Action 2")

def vendor_lookup():
    webbrowser.open_new_tab(url='https://api.macvendors.com/' + RAWMAC)

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
context_menu.add_command(label="Action 3", command=action2)
context_menu.add_command(label="Action 4", command=action2)
context_menu.add_command(label="Action 5", command=action2)
context_menu.add_command(label="Lookup Vendor", command=vendor_lookup)

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

def get_raw_mac(s):
  return s.translate(str.maketrans("", "", strip_chars))

def get_clipboard():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
    except:
        print('Unsupported clipboard data')
        win32clipboard.CloseClipboard()
    else:
        return data

def set_clipboard(s):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(s)
        win32clipboard.CloseClipboard()
    except:
        print('An error occured')
        win32clipboard.CloseClipboard()



icon_thread = threading.Thread(target=create_systray)
icon_thread.start()

keyboard.add_hotkey('ctrl+alt+shift+m', show_menu)

custom_tkinter_loop()

icon_thread.join()

