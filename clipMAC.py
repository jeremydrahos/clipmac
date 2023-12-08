"""
pystray: systray libary
PIL: python image library
keyboard: hotkey library
threading: threading, to alow multiple functions to run concurrently
tkinter: TK interface for menu
time: sleep function
webbrowser: open url in default browser for vendor lookup
win32clipboard: manage clipboard data
os: file/directory management
requests: http requests for vendor lookup
logging: logging to file
"""

from tkinter import Menu
import threading
import tkinter as tk
import time
import webbrowser
import keyboard
import win32clipboard
import os
import logging
from requests import get
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image

VERSION = '0.1.3'
RAWMAC = ''
LOCALAPPDIR = os.getenv('LOCALAPPDATA') + '\\clipMAC\\'
LOGFILE = LOCALAPPDIR + 'clipMAC.log'
image = Image.open('clipmac.png')
show_menu_flag = False
exit_flag = False
strip_chars = ":-. "
clipboard_data = ''
context_menu = None
HOTKEY = 'ctrl+alt+shift+m'

def init_dir_and_log():
    global LOCALAPPDIR, LOGFILE
    if not os.path.exists(LOCALAPPDIR):
        print('Application directory does not exist.  Creating.')
        try:
            os.makedirs(LOCALAPPDIR)
        except Exception as e:
            print(f'An exception occured: {e}')

    if not os.path.exists(LOGFILE):
        print('Log file does not exist.  Creating.')
        try:
            with open(LOGFILE, 'w', encoding='utf-8') as logfile:
                logfile.write(f'Version: {VERSION}\n')
        except Exception as e:
            print(f'An exception occured: {e}')

init_dir_and_log()
logging.basicConfig(filename=LOGFILE, level=logging.INFO, style='{', datefmt='%Y-%m-%d %H:%M:%S', format='{asctime} {levelname} {filename}:{lineno}: {message}')

def menu_ver():
    return 'clipMAC v' + str(VERSION)

def get_vendor():
    global RAWMAC
    try:
        vendor = get('https://api.macvendors.com/' + RAWMAC)
        if vendor.status_code == 404:
            return 'Vendor: Not Found'
            logging.info(f'Vendor lookup failed for {RAWMAC}')
        return f'Vendor: {vendor.text}'
    
    except Exception as e:
        logging.error(f'An exception occured in get_vendor(): {e}')
        return 'Vendor lookup failed'

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
    logging.info('Exiting via quit_clicked')
    icon.stop()
    exit_flag = True
    
def on_hotkey():
    global show_menu_flag
    show_menu_flag = True

def get_raw_mac(s):
  return s.translate(str.maketrans("", "", strip_chars))

def get_clipboard():
    global RAWMAC, clipboard_data
    win32clipboard.OpenClipboard()
    
    try:
        clipboard_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

    except Exception as e:
        logging.error(f'Exception in get_clipboard: {e}\nclipboard_data: {clipboard_data}')
        win32clipboard.CloseClipboard()

    else:
        RAWMAC = get_raw_mac(clipboard_data)
        if len(RAWMAC) != 12:
            RAWMAC = 'invalid'
            
        else:
            RAWMAC = RAWMAC.lower()
            return RAWMAC.lower()

def set_clipboard(s):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(s)
        win32clipboard.CloseClipboard()
        
    except Exception as e:
        logging.error(f'An error occured in set_clipboard: {e}\nReceived data was: {s}')
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
    
    if context_menu is not None:
        get_clipboard()
        time.sleep(0.5)
        context_menu.destroy()

    if RAWMAC == '':
        get_clipboard()
     
    if len(RAWMAC) == 12:
        context_menu = Menu(root, tearoff=0)
        context_menu.add_command(label=RAWMAC, command=copy_raw_lower)
        context_menu.add_command(label=RAWMAC.upper(), command=copy_raw_upper)
        context_menu.add_command(label=show_mac_colon_upper(), command=copy_colon_upper)
        context_menu.add_command(label=show_mac_colon_lower(), command=copy_mac_colon_lower)
        context_menu.add_command(label=show_mac_dot(), command=copy_mac_dot)
        context_menu.add_command(label=show_mac_dash(), command=copy_mac_dash)
        context_menu.add_command(label=show_mac_splunk(), command=copy_mac_splunk)
        context_menu.add_command(label=get_vendor(), command=vendor_lookup)
        context_menu.add_separator()
        context_menu.add_command(label='Oops... close menu', command=context_menu.unpost)
        x, y = root.winfo_pointerxy()
        root.after(0, context_menu.post(x, y))
        show_menu_flag = True
               
    else:
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

logging.info(f'clipMAC v{VERSION} started')

icon_thread = threading.Thread(target=create_systray)
icon_thread.start()

keyboard.add_hotkey(HOTKEY, on_hotkey)

custom_tkinter_loop()

icon_thread.join()
