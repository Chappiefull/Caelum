import asyncio
import weakref

import flet as ft


def formatar(segundos: int) -> str:
    return f"{segundos // 60:02d}:{segundos % 60:02d}"


class Cronometro:
    def __init__(self, page: ft.Page):
        self.page = page
        self.segundos = 0
        self.rodando = False
        self.geracao = 0
        self.cartao: ft.Container | None = None
        self.texto: ft.Text | None = None
        self.nome: ft.Text | None = None

    def alternar(self, e=None) -> None:
        self.rodando = not self.rodando
        if self.rodando:
            self.geracao += 1
            self.page.run_task(self._contar, self.geracao)
        self.pintar()

    def parar(self) -> None:
        self.rodando = False

    def resetar(self) -> None:
        self.segundos = 0
        self.rodando = False
        self.geracao += 1
        if self._montado():
            self.texto.value = formatar(0)
            self.texto.update()
            self.pintar()

    def pintar(self) -> None:
        self.cartao.bgcolor = (
            ft.Colors.PRIMARY if self.rodando else ft.Colors.PRIMARY_CONTAINER
        )
        frente = ft.Colors.ON_PRIMARY if self.rodando else None
        self.texto.color = frente
        self.nome.color = frente
        self.cartao.update()

    def _montado(self) -> bool:
        controle = self.texto
        while controle is not None and not isinstance(controle, ft.View):
            controle = controle.parent
        return controle is not None and any(
            controle is v for v in self.page.views
        )

    async def _contar(self, geracao: int) -> None:
        while self.rodando and geracao == self.geracao:
            await asyncio.sleep(1)
            if not self.rodando or geracao != self.geracao:
                return
            self.segundos += 1
            if self._montado():
                self.texto.value = formatar(self.segundos)
                self.texto.update()


_registro: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()


def obter(page: ft.Page, materia: str) -> Cronometro:
    por_materia = _registro.get(page)
    if por_materia is None:
        por_materia = {}
        _registro[page] = por_materia
        _vigiar(page, por_materia)
    if materia not in por_materia:
        por_materia[materia] = Cronometro(page)
    return por_materia[materia]


def parar(page: ft.Page) -> None:
    for crono in _registro.get(page, {}).values():
        crono.parar()


def _vigiar(page: ft.Page, por_materia: dict[str, Cronometro]) -> None:
    anterior = getattr(page, "on_disconnect", None)

    def ao_desconectar(e):
        for crono in por_materia.values():
            crono.parar()
        _registro.pop(page, None)
        if anterior is not None:
            anterior(e)

    page.on_disconnect = ao_desconectar
