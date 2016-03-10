import sys
import time
import BaseHTTPServer
#import SimpleHTTPServer
import PythonFBX
import os
#import glob
from SimpleHTTPServer import SimpleHTTPRequestHandler

HandlerClass = SimpleHTTPRequestHandler
ServerClass = BaseHTTPServer.HTTPServer
Protocol = 'HTTP/1.0'

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('localhost',port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address,HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
os.system("PythonFBX.py 1")
httpd.serve_forever()

#svgFilenames = []

#def getSVG():
#    del svgFilenames[:]
#    for file in glob.glob("*.svg"):
#        svgFilenames.append(file)
#    print("there is %s" % len(svgFilenames))

#class svgHandler(BaseHTTPServer.BaseHTTPRequestHandler):
#    def hostSVG(svg):
#        getSVG()
#        path = os.getcwd()
#        for file in svgFilenames:
#            f = open(file)
#            svg.send_response(200)
#            svg.send_header("Content-type", "image/svg+xml")
#            svg.end_headers()
#            svg.wfile.write(f.read())
#            f.close()

#class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):      
#    def do_GET(s):
#        os.system("PythonFBX.py 1")
#        getSVG()
#        #path = os.getcwd()
#        #for file in svgFilenames:
#        #    f = open(file)
#        #    s.send_response(200)
#        #    s.send_header("Content-type", "image/svg+xml")
#        #    s.end_headers()
#        #    s.wfile.write(f.read())
#        #    f.close()
#        s.send_response(200)
#        s.send_header("Content-type", "text/html")
#        s.end_headers()
#        #for file in glob.glob("*.html"):
#        #    f = open(file)
#        #    s.wfile.write(f.read())
#        #    f.close()
#        s.wfile.write("<html><head><title>FBX Viewer.</title></head>")
#        s.wfile.write("<body><p>This is my FBX viewer!.</p>")
#        for file in range(len(svgFilenames)):
#            s.wfile.write("<a href=" + str(svgFilenames[file]) + ">Link to SVG file</a>")
#            s.wfile.write("\n")
#        s.wfile.write("</body></html>")

    


#httpd = BaseHTTPServer.HTTPServer(("localhost", 8000), myHandler)
#httpd.serve_forever()

#for file in svgFilenames:
#    httpsvg = BaseHTTPServer.HTTPServer(("http://" + str(svgFilenames[file]), 8000), svgHandler)
#    httpsvg.serve_forever()