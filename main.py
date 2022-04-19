# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from web_service import Web_Service

hostName = "localhost"
serverPort = 8080

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), Web_Service)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")