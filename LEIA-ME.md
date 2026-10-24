# Exercício 7.3 — Multicamadas em Python

Execute `python3 app.py` no terminal do Codespaces. Abra **Ports > 8000 > Open in Browser**.

As quatro camadas são:
1. **Apresentação** — `view.py`
2. **Aplicação** — `controller.py` + `servidor.py`
3. **Negócio** — `service.py`
4. **Dados** — `repository.py` (SQLite).

Nova funcionalidade: adicionar/remover livros da **lista de desejos**. Mantém busca, preço, estoque e reservas por 24h. Dados fictícios, demonstrativo de um usuário local.
