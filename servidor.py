from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse, urlencode

class Handler(BaseHTTPRequestHandler):
    def responder(self, html):
        data = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        from controller import pagina
        query = parse_qs(urlparse(self.path).query)
        self.responder(pagina(query.get('busca',[''])[0], query.get('mensagem',[''])[0]))

    def do_POST(self):
        from controller import acao
        tamanho = int(self.headers.get('Content-Length','0'))
        form = parse_qs(self.rfile.read(tamanho).decode('utf-8'))
        try:
            id = int(form.get('id',['0'])[0])
            texto = acao(urlparse(self.path).path, id)
        except (ValueError, KeyError) as e:
            texto = str(e) or 'Não foi possível completar a ação.'
        self.send_response(303)
        self.send_header('Location','/?'+urlencode({'mensagem':texto}))
        self.end_headers()

def executar():
    print('Abra a porta 8000 no Codespaces para ver o aplicativo.')
    ThreadingHTTPServer(('0.0.0.0',8000),Handler).serve_forever()
