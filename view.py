MOSTRAR_DESEJOS = True
from html import escape

CSS = """*{box-sizing:border-box}body{margin:0;background:#f6f5f0;color:#26342c;font:16px system-ui,Arial}main{max-width:950px;margin:30px auto;padding:0 20px}header{background:#164b39;color:#fff;padding:28px}header h1{margin:0}h2{font-size:21px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:14px}.card{background:white;border:1px solid #e0e5df;border-radius:15px;padding:19px}.card h3{margin:0 0 5px}small,.muted{color:#69766f}.preco{font-size:21px;font-weight:700;color:#164b39}button{background:#166b4d;color:white;border:0;border-radius:8px;padding:11px 15px;cursor:pointer}button:disabled{background:#aaa;cursor:default}input{padding:12px;border:1px solid #bbb;border-radius:9px;width:min(430px,100%)}.search{display:flex;gap:8px;margin:20px 0}.error{background:#fff3d4;padding:12px;border-radius:8px}.footer{margin:35px 0;color:#69766f}.tag{color:#14734a;font-size:14px}form{display:inline}.row{display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 0}section{margin:27px 0}"""


def renderizar(livros, reservas, termo="", mensagem="", desejos=None):
    desejos = desejos or []
    blocos = []
    for livro in livros:
        id = livro['id']
        titulo = escape(livro['titulo'])
        autor = escape(livro['autor'])
        reservado = bool(livro['reservado'])
        disponivel = livro['disponivel']
        texto = 'Já reservado' if reservado else ('Indisponível' if disponivel < 1 else 'Reservar por 24h')
        disabled = 'disabled' if reservado or disponivel < 1 else ''
        wish = ''
        if desejos is not None and MOSTRAR_DESEJOS:
            marcado = id in desejos
            wish = f'<form method="post" action="/desejo"><input type="hidden" name="id" value="{id}"><button style="background:#805e7b">{"♥ Remover dos desejos" if marcado else "♡ Adicionar aos desejos"}</button></form>'
        blocos.append(f"""<article class="card"><h3>📚 {titulo}</h3><div class="muted">{autor}</div><p class="preco">R$ {livro['preco']:.2f}</p><p class="tag">{disponivel} exemplar(es) disponíveis</p><form method="post" action="/reservar"><input type="hidden" name="id" value="{id}"><button {disabled}>{texto}</button></form> {wish}</article>""")
    res = ''.join(f'<div class="row"><span><strong>{escape(r["titulo"])}</strong> — até {escape(r["expira_em"][:16].replace("T", " "))} (UTC)</span><form method="post" action="/cancelar"><input type="hidden" name="id" value="{r["livro_id"]}"><button>Cancelar</button></form></div>' for r in reservas)
    avisos = '<section><h2>Minha lista de desejos</h2>'+(''.join('<p>♥ '+escape(l['titulo'])+'</p>' for l in livros if l['id'] in desejos) or '<p>Sem livros na lista.</p>')+'</section>' if MOSTRAR_DESEJOS else ''
    return f"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Minha Livraria</title><style>{CSS}</style></head><body><header><main style="margin:0 auto"><h1>📖 Minha Livraria</h1><p>Encontre livros, consulte o estoque e reserve seu exemplar.</p></main></header><main>{'<p class="error">'+escape(mensagem)+'</p>' if mensagem else ''}<form class="search" method="get" action="/"><input type="search" name="busca" placeholder="Buscar título ou autor" value="{escape(termo,quote=True)}"><button>Buscar</button></form><section><h2>Catálogo</h2><div class="grid">{''.join(blocos) or '<p>Nenhum livro encontrado.</p>'}</div></section><section><h2>Minhas reservas</h2>{res or '<p>Nenhuma reserva ativa.</p>'}</section>{avisos}<p class="footer">Projeto acadêmico • estoque ilustrativo • reservas salvas em SQLite no servidor local.</p></main></body></html>"""
