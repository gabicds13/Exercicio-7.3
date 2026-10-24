import service
from view import renderizar

def pagina(termo, mensagem):
    livros, reservas, desejos = service.estado(termo)
    return renderizar(livros, reservas, termo, mensagem, desejos)

def acao(rota, id):
    return service.processar(rota, id)
