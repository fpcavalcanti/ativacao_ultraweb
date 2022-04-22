from http.server import BaseHTTPRequestHandler
import json

class Web_Service(BaseHTTPRequestHandler):
    def _set_headers(self, forbidden = True):
        if forbidden:
            self.send_response(403)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self, forbidden = True):
        self._set_headers(forbidden)

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        if (self.path == '/do_ativa'):
            self.do_HEAD(False)
            self.handle_webhook()
        else:
            self.do_HEAD(True)
            self.handle_forbidden()

    def handle_webhook(self):
        print('handling ativacao!')
        self.wfile.write(bytes(json.dumps({'status': True, 'received': 'ok'}), "utf-8"))

    def handle_forbidden(self):
        print('handling forbidden!')
        self.wfile.write(bytes(json.dumps({'status': False, 'message': 'Nao reconheco'}), "utf-8"))