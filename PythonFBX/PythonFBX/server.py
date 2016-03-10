import sys
import time
import BaseHTTPServer
import PythonFBX
import os
from SimpleHTTPServer import SimpleHTTPRequestHandler

#Server file to host the directory online which loads index.html file

HandlerClass = SimpleHTTPRequestHandler
ServerClass = BaseHTTPServer.HTTPServer
Protocol = 'HTTP/1.0'

#Sets te server address and port
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('localhost',port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address,HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."

#Runs the pythong script to create svg files and index.html
os.system("PythonFBX.py 1")
httpd.serve_forever()