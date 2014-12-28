#!/usr/local/bin/python
# coding: utf-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import building

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class Handler(BaseHTTPRequestHandler):

    def send_file(self, mimetype, path):
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


    def room_list(self):
        rooms = building.getRooms()

        self.send_response(200)
        self.send_header('Content-type', "text/html")
        self.end_headers()

        # TODO refactor in page_start and page_end
        # TODO add <html>, etc tags

        self.wfile.write('<!doctype html>')
        self.wfile.write('<title>Informant</title>')
        self.wfile.write('<link rel=stylesheet type=text/css href="/style.css">')
        self.wfile.write('<div class=page>')
        self.wfile.write('<div class="top"><div class="top-title">Rooms</div></div>')
        self.wfile.write('<ul>')

        for room in rooms:
            self.wfile.write('<li><a href=Room_%s>%s</a></li>' % (room.name, room.name))

        self.wfile.write('</ul>')
        self.wfile.write('</div>')

    
    # Handler for the GET requests
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        if self.path == '/index.html':
            self.room_list()
        
        elif self.path == '/style.css':
            mimetype='text/css'
            self.send_file(mimetype, self.path)

        elif self.path.startswith('/Room_'):
            pass
            # TODO

        elif self.path == '/weather.json':
            mimetype = 'application/json'
            # TODO

        else:
            self.send_error(404,'Not Found: %s' % self.path)


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
