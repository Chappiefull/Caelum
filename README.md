# Caelum

Aplicativo desktop para **organização, planejamento e acompanhamento de estudos**
pessoais: agenda semanal, cronômetro por matéria e flashcards em um único lugar.

## Funcionalidades

- **Agenda semanal** — grade de 7 dias × 3 períodos (dia/tarde/noite) para
  agendar matérias, com o dia corrente destacado
- **Matérias** — criar, renomear e excluir (menu de contexto no cartão)
- **Baralhos** — dentro de cada matéria, criar/renomear/excluir baralhos de
  flashcards, com contador de perguntas e botão de execução rápida
- **Flashcards** — pares pergunta/resposta com busca, ordem aleatória e modo
  "inverter" (responder a resposta)
- **Modo execução** — apresentação card a card do baralho
- **Cronômetro por matéria** — inicia/pausa/reset, continua contando mesmo
  ao navegar entre telas

## Tecnologias

- [Python](https://www.python.org/) 3.14
- [Flet](https://flet.dev/) 0.86.5
- Persistência em arquivos JSON + pastas (`data/`), sem banco de dados

## Como executar

Requisitos: Python 3.14 ou superior.

```bash
git clone https://github.com/Chappiefull/Caelum.git
cd Caelum
pip install -r requirements.txt
python app.py
```

## Estrutura do projeto

```
Caelum/
├── app.py                    entrypoint: rotas e pilha de navegação
├── armazenamento.py          I/O de disco (JSON e pastas) — único que toca o disco
├── cronometro.py             estado de sessão: cronômetro por matéria
├── requirements.txt
├── tela_inicial/             matérias e agenda de estudo
├── tela_materia/             baralhos da matéria + cronômetro do cabeçalho
├── tela_flashcard/           perguntas/respostas do baralho
└── tela_execucao/            modo execução (card a card)
```

Cada pasta `tela_*/` separa `backend.py` (regras e dados, Python puro) dos
arquivos de interface (Flet).

## Dados

Os dados do usuário ficam em `data/`, criada automaticamente na primeira
execução — uma pasta por matéria, um arquivo `.json` por baralho, além de
`data/agenda.json`. Por serem arquivos abertos e legíveis no próprio disco,
ficam diretamente acessíveis ao usuário, que pode visualizá-los, copiá-los ou
levá-los para outra máquina. O conteúdo de `data/` não faz parte do repositório.
