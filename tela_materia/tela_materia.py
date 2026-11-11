import flet as ft

import cronometro
from tela_materia import backend, dialogos, flashcards, timer

ROUTE = "/materia"
ROTA_FLASHCARD = "/flashcard"
ROTA_EXECUCAO = "/execucao"


def view(page: ft.Page, **params) -> ft.View:
    materia = params.get("materia", "")
    crono = cronometro.obter(page, materia)
    v = ft.View(
        route=ROUTE,
        padding=15,
        appbar=ft.AppBar(title=ft.Text(materia)),
        floating_action_button=ft.FloatingActionButton(
            "Criar baralho",
            width=200,
            on_click=lambda e: page.show_dialog(
                dialogos.dialog_criar_flashcard(
                    page, lambda nome: criar(page, v, materia, nome)
                )
            ),
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_FLOAT,
    )
    v.data = crono
    montar(page, v, materia)
    return v


def montar(page: ft.Page, v: ft.View, materia: str) -> None:
    v.controls = [
        ft.Row(controls=[timer.timer(materia, v.data)]),
        ft.Divider(thickness=0.1, color=ft.Colors.OUTLINE),
        ft.Container(
            width=float("inf"),
            alignment=ft.Alignment.CENTER,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Row(
                        wrap=True,
                        spacing=12,
                        run_spacing=12,
                        controls=[
                            flashcards.flashcard(
                                nome,
                                backend.contar_perguntas(materia, nome),
                                on_play=(
                                    lambda e, n=nome: page.navigate(
                                        ROTA_EXECUCAO,
                                        materia=materia,
                                        flashcard=n,
                                        indice=0,
                                        origem="materia",
                                    )
                                ),
                                on_click=(
                                    lambda e, n=nome: page.navigate(
                                        ROTA_FLASHCARD, materia=materia, flashcard=n
                                    )
                                ),
                                on_editar=(
                                    lambda e, n=nome: editar(page, v, materia, n)
                                ),
                                on_excluir=(
                                    lambda e, n=nome: confirmar_exclusao(
                                        page, v, materia, n
                                    )
                                ),
                            )
                            for nome in backend.listar_flashcards(materia)
                        ],
                        margin=ft.Margin.only(bottom=80),
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
    ]


def criar(page: ft.Page, v: ft.View, materia: str, nome: str) -> None:
    backend.criar_flashcard(materia, nome)
    atualizar(page, v, materia)


def editar(page: ft.Page, v: ft.View, materia: str, nome: str) -> None:
    page.show_dialog(
        dialogos.dialog_editar_flashcard(
            page,
            nome,
            lambda novo: renomear(page, v, materia, nome, novo),
        )
    )


def renomear(page: ft.Page, v: ft.View, materia: str, antigo: str, novo: str) -> None:
    backend.renomear_flashcard(materia, antigo, novo)
    atualizar(page, v, materia)


def confirmar_exclusao(page: ft.Page, v: ft.View, materia: str, nome: str) -> None:
    page.show_dialog(
        dialogos.dialog_excluir_flashcard(
            page, nome, lambda: excluir(page, v, materia, nome)
        )
    )


def excluir(page: ft.Page, v: ft.View, materia: str, nome: str) -> None:
    backend.excluir_flashcard(materia, nome)
    atualizar(page, v, materia)


def atualizar(page: ft.Page, v: ft.View, materia: str) -> None:
    montar(page, v, materia)
    page.update()


def main(page: ft.Page) -> None:
    page.title = "Matéria"
    page.views.append(view(page, materia="Biologia"))
    page.update()


if __name__ == "__main__":
    ft.run(main)
