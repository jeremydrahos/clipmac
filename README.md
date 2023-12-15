# clipMAC

The purpose of this utility is that I was frustrated with dealing with MAC addresses in so many different formats from different systems, ie. Cisco dotted format, colon uppercase or lowercase formats, dashed formats, etc.
This application runs in the system tray and listens for a hotkey (default is ```ctrl+alt+shift+m```), it then pops up a context menu whereever your mouse pointer is with the formatting-stripped MAC address, then offers options to copy it in the selected format.  It also provides real-time vendor lookup.
Furthermore, I am often looking into DHCP exchanges in Splunk, so I've added the "[MAC] AND DHCP" menu option to quickly find what I'm looking for, regardless of where I got the MAC address, ie. Cisco, which would require reformatting.

### Menu Sample
![clipMAC Sample](https://github.com/jeremydrahos/clipmac/blob/master/example.png?raw=true)

_In this example, I had copied a MAC that was lowercase with colons._