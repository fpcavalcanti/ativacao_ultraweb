from http.server import BaseHTTPRequestHandler
import json

class Web_Service(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        if (self.path == '/do_ativa'):
            self.handle_webhook()
        else:
            print('!')

    def handle_webhook(self):
        print('handling ativacao!')
        self.wfile.write(bytes(json.dumps({'status': True, 'received': 'ok'}), "utf-8"))