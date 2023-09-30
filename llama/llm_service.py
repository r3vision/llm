from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
from subprocess import PIPE
import time
from threading import Timer
import os
import requests

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'do_GET': 'OK'}).encode('utf-8'))

    def do_POST(self):    
        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        payload_string = self.rfile.read(length).decode('utf-8')
        message = json.loads(payload_string) if payload_string else None
        print('POST Request:(%s)' % message)

        if message is None or not message['data']:
            self._set_headers()
            self.wfile.write(bytes('Empty').encode('utf-8'))
            print('\n')
            return
 
        result_arr = []
        row_idx = 0
        for row in message['data']:
            row_val = row[1]
            t = row_val.split()
            res = 'Unrecognized command, try PING (manual mode)'
            if t[0] == 'PING':
                v = ''
                try:
                    v = 'PONG'
                except:
                    v = 'ping error'
                res = v
            if t[0] == 'TAIL':
                v = ""
                lines = t[1]
                file = t[2]
                proc = subprocess.Popen(["tail", "-"+lines, file], stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
                output, err = proc.communicate()
                if err:
                    v = err.decode()
                else:
                    v = output.decode()
                res = v
            if t[0] == 'RUN':
                v = ''
                try:
                    print('RUN command', flush=True)
                    print('rowval ',row_val, flush=True)
                    print('rowval:4 ',row_val[4:], flush=True)
                    v = subprocess.Popen(row_val[4:], shell=True, stdout=subprocess.PIPE).stdout.read().decode('ascii')
                    print('v ',v, flush=True)
                except:
                    v = 'command failed to run'
                    print('failed-v ',v, flush=True)
                res = v
            out_row = [row_idx, res]
            result_arr.append(out_row)
            row_idx += 1

        result_content = {'data': result_arr}
        print('Results: %s' % result_content)

        # send the prediction results back
        self._set_headers()
        self.wfile.write(json.dumps(result_content).encode('utf-8'))
        print('\n')

if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started at http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
