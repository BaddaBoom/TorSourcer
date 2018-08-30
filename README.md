# TorSourcer
Pull a Tor page down without FF and scrub it for mal-chars.

### **About**
Sometimes, people add characters to their onion sites that FireFox (Tor Browser Bundle version) just cant handle, and since you (if you're doing it right) have everything in FireFox turned off/unavailable then you probably have error handling turned off and thus, FF will crash. Perhaps it was just a mistake that a non-English-speaking person added, or maybe its something worse, like a site that is testing exploits (true story). Using this tool, you can scrape a web site on Tor and sanitize the non-ASCII characters out. 

### **Usage**
torsourcer.py \<Tor address\> \<output file\>

The Tor address needs to be an HTTPS (if its not set as the protocol it will be prepended) and end with the proper .onion TLD. The **\<output file\>** is a text file. 

### **Notes**
Tor needs to be running. The script has 127.0.0.1:9150 hardcoded by default, but if your instance is different then please change the marked line accordingly.
Any non-ASCII (code = \>128) will be replaced by \<\<code\>\>. Example is Ñ -> \<\<209\>\>.
