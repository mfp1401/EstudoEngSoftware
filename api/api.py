from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/hello':
            self._set_headers()
            response = {'message': 'Hello World!'}
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)
            response = {'error': 'Rota não encontrada'}
            self.wfile.write(json.dumps(response).encode())

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f'Servidor rodando na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()