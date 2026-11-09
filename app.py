from urllib.parse import parse_qs, urlparse

import flet as ft

import cronometro
from tela_execucao import tela_execucao
from tela_flashcard import tela_flashcard
from tela_inicial import tela_inicial
from tela_materia import tela_materia

TELAS = {
    tela_inicial.ROUTE: tela_inicial.view,
    tela_materia.ROUTE: tela_materia.view,
    tela_flashcard.ROUTE: tela_flashcard.view,
    tela_execucao.ROUTE: tela_execucao.view,
}


def separar(rota: str) -> tuple[str, dict[str, str]]:
    partes = urlparse(rota)
    parametros = {chave: valores[0] for chave, valores in parse_qs(partes.query).items()}
    return partes.path or "/", parametros


def main(page: ft.Page) -> None:
    page.title = "Caelum"
    historico: list[str] = []

    def construir(rota: str) -> ft.View:
        caminho, parametros = separar(rota)
        tela = TELAS.get(caminho, TELAS[tela_inicial.ROUTE])
        v = tela(page, **parametros)
        v.route = rota
        return v

    def reconstruir() -> None:
        page.views.clear()
        page.views.extend(construir(rota) for rota in historico)
        page.update()

    def tratar_rota(rota: str) -> None:
        if separar(rota)[0] == tela_inicial.ROUTE:
            cronometro.parar(page)
        if rota in historico:
            historico[:] = historico[: historico.index(rota) + 1]
            reconstruir()
            return
        historico.append(rota)
        page.views.append(construir(rota))
        page.update()

    def ao_mudar_rota(e):
        tratar_rota(e.route)

    def ao_voltar(e):
        if len(historico) <= 1:
            return
        if e.view is not None and historico[-1] != e.view.route:
            return
        historico.pop()
        reconstruir()
        if historico:
            page.navigate(historico[-1])

    page.on_route_change = ao_mudar_rota
    page.on_view_pop = ao_voltar
    page.views.clear()
    tratar_rota(page.route)


if __name__ == "__main__":
    ft.run(main)
