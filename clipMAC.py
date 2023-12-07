"""
pystray: systray libary
PIL: python image library
keyboard: hotkey library
threading: threading, to alow multiple functions to run concurrently
tkinter: TK interface for menu
time: sleep function
webbrowser: open url in default browser for vendor lookup
win32clipboard: manage clipboard data
"""

from asyncio.windows_events import NULL
from multiprocessing import context
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
strip_chars = ":-. "
clipboard_data = ''
context_menu = None

def fart():
    print('fart')

def menu_ver():
    return 'clipMAC v' + str(VERSION)

def show_mac_colon_upper():
    global RAWMAC
    return f'{RAWMAC[0]}{RAWMAC[1]}:{RAWMAC[2]}{RAWMAC[3]}:{RAWMAC[4]}{RAWMAC[5]}:{RAWMAC[6]}{RAWMAC[7]}:{RAWMAC[8]}{RAWMAC[9]}:{RAWMAC[10]}{RAWMAC[11]}'.upper()

def show_mac_colon_lower():
    global RAWMAC
    return f'{RAWMAC[0]}{RAWMAC[1]}:{RAWMAC[2]}{RAWMAC[3]}:{RAWMAC[4]}{RAWMAC[5]}:{RAWMAC[6]}{RAWMAC[7]}:{RAWMAC[8]}{RAWMAC[9]}:{RAWMAC[10]}{RAWMAC[11]}'.lower()

def show_mac_dot():
    global RAWMAC
    return f'{RAWMAC[0]}{RAWMAC[1]}{RAWMAC[2]}{RAWMAC[3]}.{RAWMAC[4]}{RAWMAC[5]}{RAWMAC[6]}{RAWMAC[7]}.{RAWMAC[8]}{RAWMAC[9]}{RAWMAC[10]}{RAWMAC[11]}'

def show_mac_dash():
    global RAWMAC
    return f'{RAWMAC[0]}{RAWMAC[1]}-{RAWMAC[2]}{RAWMAC[3]}-{RAWMAC[4]}{RAWMAC[5]}-{RAWMAC[6]}{RAWMAC[7]}-{RAWMAC[8]}{RAWMAC[9]}-{RAWMAC[10]}{RAWMAC[11]}'

def show_mac_splunk():
    global RAWMAC
    return f'{RAWMAC[0]}{RAWMAC[1]}:{RAWMAC[2]}{RAWMAC[3]}:{RAWMAC[4]}{RAWMAC[5]}:{RAWMAC[6]}{RAWMAC[7]}:{RAWMAC[8]}{RAWMAC[9]}:{RAWMAC[10]}{RAWMAC[11]} AND DHCP'

def copy_raw_lower():
    global RAWMAC
    set_clipboard(RAWMAC.lower())

def copy_raw_upper():
    global RAWMAC
    set_clipboard(RAWMAC.upper())

def copy_colon_upper():
    global RAWMAC
    set_clipboard(show_mac_colon_upper())

def copy_mac_colon_lower():
    global RAWMAC
    set_clipboard(show_mac_colon_lower())

def copy_mac_dot():
    global RAWMAC
    set_clipboard(show_mac_dot())
    
def copy_mac_dash():
    global RAWMAC
    set_clipboard(show_mac_dash())
    
def copy_mac_splunk():
    global RAWMAC
    set_clipboard(show_mac_splunk())
    
def vendor_lookup():
    webbrowser.open_new_tab(url='https://api.macvendors.com/' + RAWMAC)

def about_clicked(icon, item):
    print(f'clipMAC v{VERSION}')

def quit_clicked(icon, item):
    global exit_flag
    icon.stop()
    exit_flag = True
    
def on_hotkey():
    global show_menu_flag
    show_menu_flag = True

def get_raw_mac(s):
  return s.translate(str.maketrans("", "", strip_chars))

def get_clipboard():
    global RAWMAC, clipboard_data
    print(f'first: {RAWMAC}')
    win32clipboard.OpenClipboard()
    try:
        clipboard_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        print(f'Try Clipboard data: {clipboard_data}')

    except Exception as e:
        print(f'Unsupported clipboard data\nActual exception: {e}')
        win32clipboard.CloseClipboard()

    else:
        RAWMAC = get_raw_mac(clipboard_data)
        if len(RAWMAC) != 12:
            print(f'Invalid MAC: {RAWMAC}')
            RAWMAC = 'invalid'
            
        else:
            RAWMAC = RAWMAC.lower()
            print(f'Valid MAC: {RAWMAC}')
            return RAWMAC.lower()

def set_clipboard(s):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(s)
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(f'An error occured: {e}')
        win32clipboard.CloseClipboard()

def create_systray():
    image = Image.open('clipmac.png')
    icon_menu = menu(
        item(menu_ver(), about_clicked),
        item('Quit', quit_clicked)
    )

    tray_icon = icon('clipMAC', image, menu=icon_menu)
    tray_icon.run()



def show_menu():
    global show_menu_flag, context_menu, RAWMAC
    print(f'first show_menu: {RAWMAC}')
    if context_menu is not None:
        get_clipboard()
        time.sleep(0.5)
        context_menu.destroy()
        print(f'after get_clipboard: {RAWMAC}')

    if len(RAWMAC) == 12:
        print(f'12: {RAWMAC}')
        context_menu = Menu(root, tearoff=0)
        context_menu.add_command(label=RAWMAC, command=copy_raw_lower)
        context_menu.add_command(label=RAWMAC.upper(), command=copy_raw_upper)
        context_menu.add_command(label=show_mac_colon_upper(), command=copy_colon_upper)
        context_menu.add_command(label=show_mac_colon_lower(), command=copy_mac_colon_lower)
        context_menu.add_command(label=show_mac_dot(), command=copy_mac_dot)
        context_menu.add_command(label=show_mac_dash(), command=copy_mac_dash)
        context_menu.add_command(label=show_mac_splunk(), command=copy_mac_splunk)
        context_menu.add_command(label="Lookup Vendor", command=vendor_lookup)
        context_menu.add_separator()
        context_menu.add_command(label='Oops... close menu', command=context_menu.unpost)
        x, y = root.winfo_pointerxy()
        root.after(0, context_menu.post(x, y))
        show_menu_flag = True
    else:
        print(f'not 12: {RAWMAC}')
        context_menu = Menu(root, tearoff=0)        
        context_menu.add_command(label="No valid MAC", command=context_menu.unpost)
        context_menu.add_separator()
        context_menu.add_command(label='Oops... close menu', command=context_menu.unpost)
        x, y = root.winfo_pointerxy()
        root.after(0, context_menu.post(x, y))
        show_menu_flag = True

root = tk.Tk()
root.withdraw()



def custom_tkinter_loop():
    global show_menu_flag, exit_flag
    while not exit_flag:
        root.update()
        if show_menu_flag:
            show_menu()
            show_menu_flag = False
        root.update()
        time.sleep(0.1)
    root.destroy()




icon_thread = threading.Thread(target=create_systray)
icon_thread.start()

keyboard.add_hotkey('ctrl+alt+shift+m', on_hotkey)

custom_tkinter_loop()

icon_thread.join()

