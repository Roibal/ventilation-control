#!/usr/local/bin/python
# coding: utf-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import building
import weathermath

import contextlib
import sqlite3
import json
import sys
from datetime import datetime

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
        self.send_response(200)
        self.send_header('Content-type', "text/html")
        self.end_headers()

        self.print_page_header(roomName)
        self.wfile.write('<div id="container" style="width:100%; height:700px;"></div>\n')
        self.wfile.write('<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n')
        self.wfile.write('<script src="http://code.highcharts.com/stock/highstock.js"></script>\n')

        host = self.headers.get('Host')

        # for info see:
        # http://stackoverflow.com/questions/24634944/highcharts-4-0-3-stacked-bar-chart-bug-adds-%C3%A2
        # http://forum.highcharts.com/highcharts-usage/problem-highcharts-tooltip-a-t30357/
        # http://www.highcharts.com/docs/chart-and-series-types/combining-chart-types
        # http://www.highcharts.com/stock/demo/candlestick-and-volume

        s = """
<script type="text/javascript">
$(function () {

    $.getJSON('http://%s/%s.json?callback=?', function (data) {
        // split the data
        var insideTemperature = [],
            insideHumidity = [],
            outsideTemperature = [],
            outsideHumidity = [],
            insideHumidityAbs = [],
            outsideHumidityAbs = [],
            dataLength = data.length,
            i = 0;

        for (i; i < dataLength; i += 1) {
            insideTemperature.push([
                data[i][0], // the date
                data[i][1]  // inside temp
            ]);

            insideHumidity.push([
                data[i][0], // the date
                data[i][2] // inside humidity
            ]);

            outsideTemperature.push([
                data[i][0], // the date
                data[i][3]  // outside temp
            ]);

            outsideHumidity.push([
                data[i][0], // the date
                data[i][4] // outside humidity
            ]);

            insideHumidityAbs.push([
                data[i][0], // the date
                data[i][5] // inside humidity abs
            ]);

            outsideHumidityAbs.push([
                data[i][0], // the date
                data[i][6] // outside humidity abs
            ]);
        }

        // Create the chart
        $('#container').highcharts('StockChart', {

            rangeSelector : {
                selected : 1
            },

            yAxis: [{
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Temperature'
                },
                height: '30%%',
                lineWidth: 2
            }, {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Humidity'
                },
                top: '33%%',
                height: '30%%',
                offset: 0,
                lineWidth: 2
            }, {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Humidity Abs'
                },
                top: '66%%',
                height: '34%%',
                offset: 0,
                lineWidth: 2
            }],

            series : [{
                type: 'line',
                name : 'Inside temperature',
                data : insideTemperature,
                yAxis: 0,
                tooltip: {
                    valueDecimals: 1,
                    pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>'
                }
            }, {
                type: 'line',
                name : 'Inside humidity',
                data : insideHumidity,
                yAxis: 1,
                tooltip: {
                    valueDecimals: 0,
                    pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>'
                }
            }, {
                type: 'line',
                name : 'Ouside temperature',
                data : outsideTemperature,
                yAxis: 0,
                tooltip: {
                    valueDecimals: 1,
                    pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>'
                }
            }, {
                type: 'line',
                name : 'Outside humidity',
                data : outsideHumidity,
                yAxis: 1,
                tooltip: {
                    valueDecimals: 0,
                    pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>'
                }
            }, {
                type: 'line',
                name : 'Inside humidity abs',
                data : insideHumidityAbs,
                yAxis: 2,
                tooltip: {
                    valueDecimals: 0,
                    pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>'
                }
            }, {
                type: 'line',
                name : 'Outside humidity abs',
                data : outsideHumidityAbs,
                yAxis: 2,
                tooltip: {
                    valueDecimals: 0,
                    pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>'
                }
            }]
        });
    });

});
</script>
""" % (host, roomName)
        self.wfile.write(s)
        self.print_room_footer()


    def send_json_data(self, roomName, callbackName):
        self.send_response(200)
        self.send_header('Content-type', 'text/javascript')
        self.end_headers()

        with contextlib.closing(sqlite3.connect('meteorologist.db',detect_types=sqlite3.PARSE_DECLTYPES)) as database:
            with contextlib.closing(database.cursor()) as cursor:
                cursor.execute( 'select date, inside_temperature, inside_humidity, outside_temperature, outside_humidity from weather where room=?', (roomName,) )
                data = []
                for date, inside_temperature, inside_humidity, outside_temperature, outside_humidity in cursor:
                    # cut seconds and microsecound, we only have 5 min resolution
                    date = date.replace(second=0, microsecond=0)
                    # convert to unix timestamp
                    timestamp = (date - datetime(1970,1,1)).total_seconds()
                    # timestamp needs to be in milliseconds
                    timestamp *= 1000

                    inside_humidity_abs = weathermath.AF(inside_humidity, inside_temperature)
                    outside_humidity_abs = weathermath.AF(outside_humidity, outside_temperature)

                    data.append( [int(timestamp), float(inside_temperature), float(inside_humidity), float(outside_temperature), float(outside_humidity), float(inside_humidity_abs), float(outside_humidity_abs)] )
        
        self.wfile.write('%s(\n' % callbackName)
        json.dump(data, self.wfile)
        self.wfile.write('\n);')

    
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

        elif '.json' in self.path:
            # get roomname and callback name (both dynamic)
            index = self.path.find('.json')
            roomName = self.path[1:index]
            # .json?callback=
            indexUnderscore = self.path.find('&_')
            callbackName = self.path[index+15:indexUnderscore]
            self.send_json_data(roomName, callbackName)

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
