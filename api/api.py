from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class APIHandler(BaseHTTPRequestHandler):
    # Simulando um banco de dados simples
    users = {}

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _read_json_data(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            return json.loads(post_data.decode('utf-8'))
        return None

    def do_GET(self):
        if self.path.startswith('/api/users/'):
            user_id = self.path.split('/')[-1]
            if user_id in self.users:
                self._set_headers()
                response = self.users[user_id]
            else:
                self._set_headers(404)
                response = {'error': 'Usuario nao encontrado'}
        else:
            self._set_headers(404)
            response = {'error': 'Rota nao encontrada'}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/api/users':
            try:
                post_data = self._read_json_data()
                if post_data is None:
                    self._set_headers(400)
                    response = {'error': 'Dados JSON nao fornecidos'}
                else:
                    # Gerar um ID simples
                    user_id = str(len(self.users) + 1)
                    self.users[user_id] = post_data
                    self._set_headers()
                    response = {
                        'message': 'Usuario criado com sucesso',
                        'id': user_id,
                        'data': post_data
                    }
            except json.JSONDecodeError:
                self._set_headers(400)
                response = {'error': 'JSON invalido'}
        else:
            self._set_headers(404)
            response = {'error': 'Rota nao encontrada'}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def do_PUT(self):
        if self.path.startswith('/api/users/'):
            user_id = self.path.split('/')[-1]
            try:
                put_data = self._read_json_data()
                if put_data is None:
                    self._set_headers(400)
                    response = {'error': 'Dados JSON nao fornecidos'}
                elif user_id not in self.users:
                    self._set_headers(404)
                    response = {'error': 'Usuario nao encontrado'}
                else:
                    # Atualiza os dados do usuario
                    self.users[user_id].update(put_data)
                    self._set_headers()
                    response = {
                        'message': 'Usuario atualizado com sucesso',
                        'id': user_id,
                        'data': self.users[user_id]
                    }
            except json.JSONDecodeError:
                self._set_headers(400)
                response = {'error': 'JSON invalido'}
        else:
            self._set_headers(404)
            response = {'error': 'Rota nao encontrada'}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def do_DELETE(self):
        if self.path.startswith('/api/users/'):
            user_id = self.path.split('/')[-1]
            if user_id in self.users:
                # Remove o usuário do dicionário
                deleted_user = self.users.pop(user_id)
                self._set_headers()
                response = {
                    'message': 'Usuario removido com sucesso',
                    'id': user_id,
                    'data': deleted_user
                }
            else:
                self._set_headers(404)
                response = {'error': 'Usuario nao encontrado'}
        else:
            self._set_headers(404)
            response = {'error': 'Rota nao encontrada'}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f'Servidor rodando na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

