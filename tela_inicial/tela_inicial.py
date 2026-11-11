import flet as ft

from tela_inicial import backend, calendario, dialogos, materias

ROUTE = "/"
ROTA_MATERIA = "/materia"

LARGURA_BOTAO = 500


def view(page: ft.Page, **params) -> ft.View:
    v = ft.View(
        route=ROUTE,
        padding=calendario.PADDING_VISTA,
        scroll=ft.ScrollMode.AUTO,
    )
    montar(page, v)
    return v


def montar(page: ft.Page, v: ft.View) -> None:
    agenda = backend.listar_agenda()
    dimensoes = calendario.medidas(page.width)
    botao = ft.OutlinedButton(
        "Criar Matéria",
        width=largura_botao(page.width),
        height=40,
        on_click=lambda e: page.show_dialog(
            dialogos.dialog_criar_materia(page, lambda nome: criar(page, v, nome))
        ),
        margin=ft.Margin.only(bottom=8),
        style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
    )
    v.data = {
        "agenda": agenda,
        "dimensoes": dimensoes,
        "botao": botao,
    }
    v.controls = [
        linha_calendario(page, v, agenda, dimensoes, page.width),
        ft.Divider(thickness=0.1, color=ft.Colors.OUTLINE),
        ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[botao],
                ),
                *[
                    materias.materia(
                        nome,
                        lambda e, n=nome: page.navigate(ROTA_MATERIA, materia=n),
                        lambda e, n=nome: editar(page, v, n),
                        lambda e, n=nome: confirmar_exclusao(page, v, n),
                    )
                    for nome in backend.listar_materias()
                ],
            ],
        ),
    ]
    page.on_resize = lambda e: redimensionar(page, v, e.width)


def linha_calendario(
    page: ft.Page,
    v: ft.View,
    agenda: dict[str, str],
    dimensoes: calendario.Medidas,
    largura_pagina: float | None,
) -> ft.Row:
    espaco = calendario.disponivel(largura_pagina)
    rolar = espaco is not None and dimensoes.largura > espaco
    return ft.Row(
        controls=[
            calendario.grade(
                agenda,
                lambda dia, periodo: selecionar(page, v, dia, periodo),
                dimensoes,
            )
        ],
        alignment=(
            ft.MainAxisAlignment.START if rolar else ft.MainAxisAlignment.CENTER
        ),
        scroll=ft.ScrollMode.AUTO if rolar else None,
    )


def largura_botao(largura_pagina: float | None) -> int:
    espaco = calendario.disponivel(largura_pagina)
    if espaco is None:
        return LARGURA_BOTAO
    return max(1, min(LARGURA_BOTAO, int(espaco)))


def redimensionar(page: ft.Page, v: ft.View, largura: float) -> None:
    if not page.views or page.views[-1] is not v:
        return
    dados = v.data
    if not dados or "agenda" not in dados:
        return
    dimensoes = calendario.medidas(largura)
    nova_largura_botao = largura_botao(largura)
    if (
        dimensoes == dados["dimensoes"]
        and nova_largura_botao == dados["botao"].width
    ):
        return
    dados["dimensoes"] = dimensoes
    dados["botao"].width = nova_largura_botao
    v.controls[0] = linha_calendario(
        page, v, dados["agenda"], dimensoes, largura
    )
    page.update()


def criar(page: ft.Page, v: ft.View, nome: str) -> None:
    backend.criar_materia(nome)
    atualizar(page, v)


def selecionar(page: ft.Page, v: ft.View, dia: str, periodo: str) -> None:
    page.show_dialog(
        dialogos.dialog_selecionar_materia(
            page,
            f"{backend.NOMES_DIAS[dia]} de {periodo}",
            backend.listar_materias(),
            backend.materia_do_slot(dia, periodo),
            lambda nome: agendar(page, v, dia, periodo, nome),
            lambda: esvaziar(page, v, dia, periodo),
        )
    )


def agendar(page: ft.Page, v: ft.View, dia: str, periodo: str, nome: str) -> None:
    backend.agendar(dia, periodo, nome)
    atualizar(page, v)


def esvaziar(page: ft.Page, v: ft.View, dia: str, periodo: str) -> None:
    backend.desagendar(dia, periodo)
    atualizar(page, v)


def editar(page: ft.Page, v: ft.View, nome: str) -> None:
    page.show_dialog(
        dialogos.dialog_editar_materia(
            page,
            nome,
            lambda novo: renomear(page, v, nome, novo),
        )
    )


def renomear(page: ft.Page, v: ft.View, antiga: str, nova: str) -> None:
    backend.renomear_materia(antiga, nova)
    atualizar(page, v)


def confirmar_exclusao(page: ft.Page, v: ft.View, nome: str) -> None:
    page.show_dialog(
        dialogos.dialog_excluir_materia(
            page,
            nome,
            lambda: excluir(page, v, nome),
        )
    )


def excluir(page: ft.Page, v: ft.View, nome: str) -> None:
    backend.excluir_materia(nome)
    atualizar(page, v)


def atualizar(page: ft.Page, v: ft.View) -> None:
    montar(page, v)
    page.update()


def main(page: ft.Page) -> None:
    page.title = "Caelum"
    page.views.clear()
    page.views.append(view(page))
    page.update()


if __name__ == "__main__":
    ft.run(main)
