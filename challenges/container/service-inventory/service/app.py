import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
FLAG = os.environ.get('FLAG', 'VARE{enumeration_beyond_default_ports}')
class Handler(BaseHTTPRequestHandler):
    server_version = 'STMU-Telemetry/1.4'
    sys_version = ''
    def do_GET(self):
        if self.path not in ('/', '/health'):
            self.send_error(404); return
        body = (f'<!doctype html><html><head><title>{FLAG}</title></head>'
                '<body><h1>Lab telemetry gateway</h1><p>Inventory status: online.</p>'
                '<p>Read the service metadata to complete the inventory.</p></body></html>').encode()
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    do_HEAD = lambda self: self.head_only()
    def head_only(self):
        self.send_response(200);self.send_header('Content-Type','text/html');self.end_headers()
if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','5000'))),Handler).serve_forever()
