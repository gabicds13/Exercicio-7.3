from datetime import datetime, timedelta, timezone
import repository as dados

def estado(termo=''):
    dados.remover_expiradas(datetime.now(timezone.utc).isoformat())
    return dados.consultar(termo), dados.ler_reservas(), dados.favoritos()

def processar(rota, id):
    livros, reservas, desejos = estado()
    livro = next((l for l in livros if l['id']==id),None)
    if not livro:
        raise ValueError('Livro não encontrado.')
    if rota == '/reservar':
        if livro['reservado'] or livro['disponivel']<=0:
            raise ValueError('Exemplar indisponível ou já reservado.')
        dados.criar_reserva(id, (datetime.now(timezone.utc)+timedelta(hours=24)).isoformat())
        return 'Livro reservado por 24 horas!'
    if rota == '/cancelar':
        dados.remover_reserva(id)
        return 'Reserva cancelada.'
    if rota == '/desejo':
        dados.alternar_favorito(id)
        return 'Lista de desejos atualizada.'
    raise ValueError('Ação desconhecida.')
