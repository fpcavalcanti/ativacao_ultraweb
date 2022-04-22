# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from web_service import Web_Service

host_name = "localhost"
server_port = 8080

if __name__ == "__main__":
    webServer = HTTPServer((host_name, server_port), Web_Service)
    print(f"Servidor iniciado http://{host_name}:{server_port}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Servidor encerrado.")