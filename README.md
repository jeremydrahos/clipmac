# clipMAC

The purpose of this utility is that I was frustrated with dealing with MAC addresses in so many different formats from different systems, ie. Cisco dotted format, colon uppercase or lowercase formats, dashed formats, etc.
This application runs in the system tray and listens for a hotkey (default is `ctrl+alt+shift+m`), it then pops up a context menu whereever your mouse pointer is with the formatting-stripped MAC address, then offers options to copy it in the selected format. It also provides real-time vendor lookup.
Furthermore, I am often looking into DHCP exchanges in Splunk, so I've added the "[MAC] AND DHCP" menu option to quickly find what I'm looking for, regardless of where I got the MAC address, ie. Cisco, which would require reformatting.

### Menu Sample

![clipMAC Sample](https://github.com/jeremydrahos/clipmac/blob/master/example.png?raw=true)

_In this example, I had copied a MAC that was lowercase with colons._

<br>

### Standalone Windows Executable

Also, within dist/clipMAC, there's a standalone exe build of the script.
If you'd like to build it yourself after reviewing the code:
`pyinstaller -i clipmac.png --nowindowed -F clipMAC.py`
_Note: you __only__ need -F if you want it to be portable.  Omit it to build it to run on the local machine._
