#!/usr/local/bin/python
# coding: utf-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class Handler(BaseHTTPRequestHandler):

    def sendFile(self, mimetype, path):
        try:
            #Open the static file requested and send it
            f = open(curdir + sep + path) 
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    
    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        if self.path == "/index.html":
            mimetype = "text/html"
            self.sendFile(mimetype, self.path)
        
        elif self.path == "/style.css":
            mimetype="text/css"
            self.sendFile(mimetype, self.path)

        elif self.path == "/weather.json":
            mimetype = "application/json"
            # TODO


try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), Handler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
