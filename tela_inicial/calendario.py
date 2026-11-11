from dataclasses import dataclass
from datetime import date

import flet as ft

from tela_inicial import backend

LARGURA_CELULA = 100
LARGURA_ROTULO = 50
ESPACAMENTO = 8

LARGURA_CELULA_MINIMA = 40
LARGURA_ROTULO_MINIMA = 30
ESPACAMENTO_MINIMO = 2

PADDING_VISTA = 15
MARGEM_SEGURANCA = 4


@dataclass(frozen=True)
class Medidas:
    celula: int = LARGURA_CELULA
    rotulo: int = LARGURA_ROTULO
    espacamento: int = ESPACAMENTO

    @property
    def largura(self) -> int:
        dias = len(backend.DIAS)
        return self.rotulo + dias * self.celula + dias * self.espacamento


MEDIDAS_PADRAO = Medidas()


def disponivel(largura_pagina: float | None) -> float | None:
    if not largura_pagina:
        return None
    return largura_pagina - 2 * PADDING_VISTA


def medidas(largura_pagina: float | None) -> Medidas:
    espaco = disponivel(largura_pagina)
    if espaco is None or espaco >= MEDIDAS_PADRAO.largura:
        return MEDIDAS_PADRAO

    dias = len(backend.DIAS)
    util = espaco - MARGEM_SEGURANCA

    celula = (util - LARGURA_ROTULO - dias * ESPACAMENTO) / dias
    celula = max(LARGURA_CELULA_MINIMA, min(LARGURA_CELULA, celula))

    rotulo = int(max(LARGURA_ROTULO_MINIMA, min(LARGURA_ROTULO, celula / 2)))
    espacamento = int(
        max(ESPACAMENTO_MINIMO, min(ESPACAMENTO, celula / 12))
    )

    celula = (util - rotulo - dias * espacamento) / dias
    celula = max(LARGURA_CELULA_MINIMA, min(LARGURA_CELULA, celula))

    return Medidas(
        celula=int(celula),
        rotulo=rotulo,
        espacamento=espacamento,
    )


def celula(
    texto: str = "",
    destaque: bool = False,
    on_click=None,
    dimensoes: Medidas = MEDIDAS_PADRAO,
) -> ft.Container:
    return ft.Container(
        content=ft.Text(
            texto,
            size=12,
            weight=ft.FontWeight.W_600,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        ),
        height=60,
        width=dimensoes.celula,
        alignment=ft.Alignment.CENTER,
        bgcolor=(
            ft.Colors.PRIMARY_CONTAINER if destaque else ft.Colors.SURFACE_CONTAINER
        ),
        border_radius=8,
        on_click=on_click,
        tooltip=texto if texto else None,
    )


def linha(
    periodo: str,
    agenda: dict[str, str],
    on_clique,
    dimensoes: Medidas = MEDIDAS_PADRAO,
) -> ft.Row:
    hoje = date.today().weekday()
    return ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(periodo, size=12, weight=ft.FontWeight.W_600),
                width=dimensoes.rotulo,
            ),
            *[
                celula(
                    agenda.get(f"{dia}/{periodo}", ""),
                    destaque=(indice == hoje),
                    on_click=(lambda e, d=dia: on_clique(d, periodo)),
                    dimensoes=dimensoes,
                )
                for indice, dia in enumerate(backend.DIAS)
            ],
        ],
        spacing=dimensoes.espacamento,
    )


def cabecalho(dimensoes: Medidas = MEDIDAS_PADRAO) -> ft.Row:
    return ft.Row(
        controls=[
            ft.Container(width=dimensoes.rotulo),
            *[
                ft.Container(
                    content=ft.Text(dia, size=12, weight=ft.FontWeight.W_600),
                    height=60,
                    width=dimensoes.celula,
                    alignment=ft.Alignment.CENTER,
                )
                for dia in backend.DIAS
            ],
        ],
        spacing=dimensoes.espacamento,
    )


def grade(
    agenda: dict[str, str],
    on_clique,
    dimensoes: Medidas = MEDIDAS_PADRAO,
) -> ft.Column:
    return ft.Column(
        controls=[
            cabecalho(dimensoes),
            *[
                linha(periodo, agenda, on_clique, dimensoes)
                for periodo in backend.PERIODOS
            ],
        ],
        spacing=dimensoes.espacamento,
    )
