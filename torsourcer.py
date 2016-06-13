#!/usr/bin/env python
#

'''
Copyright 2015 @BaddaBoom

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

This script downloads a Tor page to a text document.
May come in useful if you are trying to get a resource that
FF cant open for whatever specified reason.
'''

import sys
import bs4
import warnings
import socket
import socks

# the following lines of code remaps the urllib connect function (dns too) to the tor proxy
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150) # Tor needs to be running. If you are using a non-standard port then change this
socks.socket.setdefaulttimeout(60)
socket.socket = socks.socksocket
socket.create_connection = create_connection

try:
    import urllib.request as urllib2    # Python 3.x
except ImportError:
    import urllib2    # Python 2.x

# uses BS4 to prettify the page
def get_data(link):
    if link[:8] != "https://":
        link = "https://" + link
    req = urllib2.Request(link)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0')
    req.add_header('Accept-Language', 'en-us,en;q=0.5')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    try:
        obj = urllib2.urlopen(req, timeout=60)
    except socks.SOCKS5Error as e:
        print("[!] ERROR: SOCKS5 timeout!")
    except urllib2.URLError as e:
        print("[!] ERROR: urllib2 timeout!")
    except socket.timeout as e:
        print("[!] ERROR: socket timeout!")
    except Exception as e:
        print("[!] ERROR: " + str(e) + "")
    else:
        header = obj.headers.get_content_charset()
        page = bs4.BeautifulSoup(obj.read(), 'html.parser').prettify(header)
        obj.close()
        return page
    return ""
    
# sift through for unsupported characters and clean them out
def clean_string(s):
    ret = ""
    for i in s:
        try:
            o = ord(i)
        except:
            o = i
        if o < 128:
            ret += str(chr(o))
        else:
            ret += "<<" + str(o) + ">>" # dont just ignore them, save them so we can see what FF dislikes so much
    return ret
    
# entry point
if __name__ == '__main__':
    print("\n TorSourcer \n:----------:")
    # u dun goofed
    if len(sys.argv) != 3:
        print("USAGE: " + sys.argv[0] + " <TOR URL> <TXT FILE>")
        print("    <TOR URL>        the site to get source from")
        print("    <TXT FILE>        the output text file to save to\n\n")
        sys.exit(1)
    site = sys.argv[1]
    print("[+] Starting.")
    sourcetxt = get_data(site)
    if len(sourcetxt) > 0:
        print("[+] Converting data.")
        content = clean_string(sourcetxt)
        print("[+] Writing data.")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(sys.argv[2], 'w+') as f:
                f.write(content)
    print("[+] Finished.\n")