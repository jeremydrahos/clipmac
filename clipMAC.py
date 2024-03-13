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
base64: encode/decode image
io: convert image to byte stream
sys: used to unload/reload keyboard module to fix issue with hotkey not working after PC locking
"""
 
from tkinter import Menu
import threading
import tkinter as tk
import time
import webbrowser
import os
import base64
import io
import logging
import keyboard
import win32clipboard
import sys
from requests import get
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image

encoded_icon = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAw3pUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBbDsMgDPvnFDsCxIGG49C1k3aDHX+BpFVZZwnnYWRCwv55v8KjgxIHzouUWkpUcOVKTROJhjY4RR48wC5pPfXDKZC2oBFWSvH7Rz+dBhaaZvliJE8X1lmo/gLJjxFZQJ+o55sbVTcCmZDcoNm3YqmyXL+w7nGG2AmdWOaxb/Wi29uyvgOiHQlRGSg2APpBQFMhKQP9YkLRnEYno7qZLuTfng6EL96pWRITaQobAAABhWlDQ1BJQ0MgcHJvZmlsZQAAeJx9kT1Iw0AcxV9bpX5UHCwiIpKhioNdVMSxVLEIFkpboVUHk0u/oElDkuLiKLgWHPxYrDq4OOvq4CoIgh8gri5Oii5S4v+SQosYD4778e7e4+4d4K2XmWJ0RABFNfVkLCpksquC/xW9GMUgujEhMkOLpxbTcB1f9/Dw9S7Ms9zP/Tn65JzBAI9AHGGabhJvEM9umhrnfeIgK4oy8TnxpE4XJH7kuuTwG+eCzV6eGdTTyXniILFQaGOpjVlRV4hniEOyolK+N+OwzHmLs1KusuY9+QsDOXUlxXWaI4hhCXEkIEBCFSWUYSJMq0qKgSTtR138w7Y/QS6JXCUwciygAgWi7Qf/g9/dGvnpKScpEAU6XyzrYwzw7wKNmmV9H1tW4wTwPQNXastfqQNzn6TXWlroCOjfBi6uW5q0B1zuAENPmqiLtuSj6c3ngfcz+qYsMHAL9Kw5vTX3cfoApKmr5Rvg4BAYL1D2usu7u9p7+/dMs78f01tyzcg11zcAAA12aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjA5MmQ4YWJlLTdjZTQtNGM4Yi1hNmY3LTZjMDFlYWVjMDI0ZSIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDozODBhZGIwYS0xZjQ4LTRkYjItODA4MS00MTlhZGI1NjczMDciCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDoyOThlZmVmOS02MjI4LTQ4MmMtYjA2OC05M2QwOWM5Zjg2MGYiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTcwMTM4MjkyMTE3ODk2NiIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjM2IgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCIKICAgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMzoxMTozMFQxNjoyMTo1OS0wNjowMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjM6MTE6MzBUMTY6MjE6NTktMDY6MDAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo3ZjJlYzU5NC0yY2MyLTQyNzItYmQ3Zi1lNzE1ODEzODA2MWMiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjMtMTEtMzBUMTY6MjI6MDEiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+CQTO5gAAAAZiS0dEAAAAAAAA+UO7fwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+cLHhYWAXO3yqQAABW7SURBVHjavZt5sGVVdcZ/e59z73vvvrHf60d3y2gzCDKIhVpaoBi0waBSCU5BMSZBiCIRUQQtpDQOlVhIOYJSUAkCKoMDKUVFYhWmIkRFhHQzl0w9QDd0091vvufstfLH3uecfc69ryWDuVXd771z791nD2ut71vfWsd0u1011oACgMGAAVXFGIOqf6P4XQ0Ypec98EMYQFE/TuMVj1l8p7geBqp9q7we36M5H8A23ovX0bxeTjJcT42pFq9+Dn0nUG5QWDzaO6noY/SsP/p881Ve12rzlP6LN6b+no02tN/4tTWEecXX0sZ7vV+gftrVehSjfpf7bUQ84X4bMjc/z69+twFxwkuPeBGTKyZ6JhnbQzF2PGbz/di6+q0jXo+IYgyYLMu0NgimZ5f930DDdItTVX905Xf6uUf8uuueDezYuYvDX3wo2IStmzby7I6dnPS6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'
icon_data = base64.b64decode(encoded_icon)
VERSION = '0.4.3'
RAWMAC = ''
LOCALAPPDIR = os.getenv('LOCALAPPDATA') + '\\clipMAC\\'
LOGFILE = LOCALAPPDIR + 'clipMAC.log'
image = Image.open(io.BytesIO(icon_data))
show_menu_flag = False
exit_flag = False
strip_chars = ":-. \t"
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
    return f'{RAWMAC[0]}{RAWMAC[1]}:{RAWMAC[2]}{RAWMAC[3]}:{RAWMAC[4]}{RAWMAC[5]}:{RAWMAC[6]}{RAWMAC[7]}:{RAWMAC[8]}{RAWMAC[9]}:{RAWMAC[10]}{RAWMAC[11]} AND DHCP*'

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
        clipboard_data = win32clipboard.GetClipboardData().replace('\n', '').replace('\r', '')
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
    image = Image.open(io.BytesIO(icon_data))
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
        context_menu.add_command(label='Close menu', command=context_menu.unpost)
        x, y = root.winfo_pointerxy()
        root.after(0, context_menu.post(x, y))
        show_menu_flag = True

    else:
        context_menu = Menu(root, tearoff=0)        
        context_menu.add_command(label="No valid MAC", command=context_menu.unpost)
        context_menu.add_separator()
        context_menu.add_command(label='Close menu', command=context_menu.unpost)
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

def listener_loop():
    global exit_flag, HOTKEY
    while not exit_flag:
        try:
            keyboard.remove_hotkey(HOTKEY)
            sys.modules.pop('keyboard')
        except:
            pass

        try:
            import keyboard
            keyboard.add_hotkey(HOTKEY, on_hotkey)
        except:
            logging.error('Keyboard module failed to load.  Retrying shortly.')
            pass

        for _ in range(4):
            time.sleep(15)
            if exit_flag:
                break

logging.info(f'clipMAC v{VERSION} started')

icon_thread = threading.Thread(target=create_systray)
listener_thread = threading.Thread(target=listener_loop)

icon_thread.start()
listener_thread.start()

custom_tkinter_loop()

icon_thread.join()
listener_thread.join()
