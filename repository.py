LIVROS_INICIAIS = [('Dom Casmurro', 'Machado de Assis', 29.9, 4), ('A Hora da Estrela', 'Clarice Lispector', 34.9, 2), ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 39.9, 0), ('Capitães da Areia', 'Jorge Amado', 32.5, 3)]

import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("livraria.db")


def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def iniciar():
    with conectar() as con:
        con.execute("CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, preco REAL, estoque INTEGER)")
        con.execute("CREATE TABLE IF NOT EXISTS reservas (livro_id INTEGER PRIMARY KEY, expira_em TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS desejos (livro_id INTEGER PRIMARY KEY)")
        if con.execute("SELECT COUNT(*) FROM livros").fetchone()[0] == 0:
            con.executemany("INSERT INTO livros (titulo,autor,preco,estoque) VALUES (?,?,?,?)", LIVROS_INICIAIS)


def consultar(termo=''):
    with conectar() as con:
        return [dict(r) for r in con.execute("""SELECT l.*, l.estoque - (SELECT COUNT(*) FROM reservas r WHERE r.livro_id=l.id) AS disponivel, (SELECT COUNT(*) FROM reservas r WHERE r.livro_id=l.id) AS reservado FROM livros l WHERE lower(l.titulo || ' ' || l.autor) LIKE lower(?) ORDER BY l.id""", ('%'+termo+'%',))]

def ler_reservas():
    with conectar() as con:
        return [dict(r) for r in con.execute("SELECT l.titulo, r.livro_id, r.expira_em FROM reservas r JOIN livros l ON l.id=r.livro_id")]

def remover_expiradas(agora):
    with conectar() as con:
        con.execute('DELETE FROM reservas WHERE expira_em <= ?', (agora,))

def criar_reserva(id, fim):
    with conectar() as con:
        con.execute('INSERT INTO reservas (livro_id,expira_em) VALUES (?,?)', (id,fim))

def remover_reserva(id):
    with conectar() as con:
        con.execute('DELETE FROM reservas WHERE livro_id=?', (id,))

def favoritos():
    with conectar() as con:
        return [r[0] for r in con.execute('SELECT livro_id FROM desejos')]

def alternar_favorito(id):
    with conectar() as con:
        if con.execute('SELECT 1 FROM desejos WHERE livro_id=?',(id,)).fetchone():
            con.execute('DELETE FROM desejos WHERE livro_id=?',(id,))
        else:
            con.execute('INSERT INTO desejos (livro_id) VALUES (?)',(id,))
