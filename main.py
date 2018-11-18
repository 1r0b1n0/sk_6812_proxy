#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import serial

ser = 0

# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        print("get : %s" % self.path )

        if str(self.path).startswith("/write="):
            writeData = str(self.path)[7:].encode('ascii')
            print("writing : %s" % writeData)
            ser.write(writeData)
            ser.flush()

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "OK"
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
    global ser
    print('starting server...')

    # Server settings
    server_address = ('0.0.0.0', 8081)
    
    # init serial
    for x in range (5):
       try:
          ser = serial.Serial('/dev/ttyLED', 9600, timeout=1)
       except serial.SerialException as e:
          print("Failed to connect, error : %s" % e.strerror)
          print("Retrying in 5 seconds")
          time.sleep(5)
       else:
           httpd = HTTPServer(server_address, RequestHandler)
           print('running server...')
           httpd.serve_forever()
           break
run()
