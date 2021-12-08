#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import od_app
import ui_sub
import threading
import subprocess

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        #ui_sub.main()
        #threading.Thread(target=ui_sub.main).start()
        #videostreamingapp.main()
        pythonuicommand = "sh serverscripts_OTA.sh"
        output = subprocess.call(['sh','./serverscripts_OTA.sh'])
        print(output)
        #uicommand = "nohup python3 videostreamingapp.py"
        #process1 = subprocess.Popen(pythonuicommand.split(), stdout=subprocess.PIPE)
        #process1 = subprocess.run(pythonuicommand, capture_output=True, shell=True, executable='/bin/bash')
        #process2 = subprocess.Popen(uicommand.split(), stdout=subprocess.PIPE)
        #output1, error1 = process1.communicate()
        #output2, error2 = process2.communicate()
        #print("Subprocess1",output1, error1)
        #print("Subprocess2",output2, error2)
        #ui_sub.main()
        #a = printcommand(self.path)
        #print(process1.stdout.decode())
        self.wfile.write("Ui sub initialized \n VS app initialized".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=5002):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        
        
        
        #watch -n 1.0 'ps -ax | grep python3'
        #docker build -t <newname> .
        
        
"""
! /bin/bash
cd "$(dirname "$0")"
echo $PATH
#export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/OpenDDS/ACE_wrappers/bin:/opt/OpenDDS/bin
source ~/.bashrc
realpath .
nohup python3 ui_pub.py &
sleep 5
nohup python3 server.py &
sleep 2
nohup /opt/dds-mqtt-bridge_b64/build/dds-mqtt videoStreaming/camFeed &
sleep 1
nohup /opt/dds-mqtt-bridge_b64/build/mqtt-dds videoStreaming/cameraRequest &
sleep 9999999999999999999999999999999999999999999999999999999999999999999999999

"""

