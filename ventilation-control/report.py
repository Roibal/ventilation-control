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


    def print_page_header(self, title):
        self.wfile.write('<!doctype html>\n')
        self.wfile.write('<html>\n')
        self.wfile.write('<head>\n')
        self.wfile.write('<title>%s</title>\n' % title)
        self.wfile.write('<link rel=stylesheet type=text/css href="/style.css">\n')
        self.wfile.write('</head>\n')
        self.wfile.write('<body>\n')
        self.wfile.write('<div class=page>\n')
        self.wfile.write('<div class="top"><div class="top-title">%s</div></div>\n' % title)

    def print_room_footer(self):
         self.wfile.write('</div>\n')
         self.wfile.write('</body>\n')
         self.wfile.write('</html>\n')


    def display_room_list(self):
        rooms = building.getRooms()

        self.send_response(200)
        self.send_header('Content-type', "text/html")
        self.end_headers()

        self.print_page_header('Rooms')

        self.wfile.write('<ul>')

        for room in rooms:
            self.wfile.write('<li><a href=Room_%s>%s</a></li>\n' % (room.name, room.name))

        self.wfile.write('</ul>')

        self.print_room_footer()
       

    def display_room(self, roomName):
        self.print_page_header(roomName)
        self.wfile.write('<div id="container" style="width:100%; height:400px;"></div>\n')
        self.wfile.write('<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n')
        self.wfile.write('<script src="http://code.highcharts.com/stock/highstock.js"></script>\n')

        s = """
<script type="text/javascript">
$(function () {

    $.getJSON('http://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function (data) {
        // Create the chart
        $('#container').highcharts('StockChart', {


            rangeSelector : {
                selected : 1
            },

            title : {
                text : 'AAPL Stock Price'
            },

            series : [{
                name : 'AAPL',
                data : data,
                tooltip: {
                    valueDecimals: 2
                }
            }]
        });
    });

});
</script>
"""
        self.wfile.write(s)
        self.print_room_footer()

    
    # Handler for the GET requests
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        if self.path == '/index.html':
            self.display_room_list()
        
        elif self.path == '/style.css':
            mimetype='text/css'
            self.send_file(mimetype, self.path)

        elif self.path.startswith('/Room_'):
            roomName = self.path[6:]
            self.display_room(roomName)

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
