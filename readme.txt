TL;DR: pip install -r requirements.txt, then python clipMAC.py

You can run the stand-alone executable, or create a virtual environment and pip install -r requirements.txt
The global hotkey uses the Windows RegisterHotKey API (stdlib ctypes), so there is no keyboard package to install.  The other requirements are for the tray icon, clipboard, vendor lookup, and pyinstaller.  You won't need pyinstaller unless you want to build your own executable after code safety review, in which case the icon (clipmac.png) has been included.