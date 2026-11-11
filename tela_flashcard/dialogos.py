import flet as ft

ALTURA_CAMPO = 3


def dialog_editar_flashcard(
    page: ft.Page, pergunta: str, resposta: str, ao_salvar, ao_excluir
) -> ft.AlertDialog:
    campo_pergunta = ft.TextField(
        label="Pergunta",
        value=pergunta,
        autofocus=True,
        multiline=True,
        min_lines=ALTURA_CAMPO,
        max_lines=ALTURA_CAMPO,
        width=400,
    )
    campo_resposta = ft.TextField(
        label="Resposta",
        value=resposta,
        multiline=True,
        min_lines=ALTURA_CAMPO,
        max_lines=ALTURA_CAMPO,
        width=400,
    )
    erro = ft.Text("", color=ft.Colors.ERROR, size=12)

    def salvar(e):
        try:
            ao_salvar(campo_pergunta.value or "", campo_resposta.value or "")
        except ValueError as falha:
            erro.value = str(falha)
            erro.visible = True
            erro.update()
            return
        page.pop_dialog()

    def cancelar(e):
        page.pop_dialog()

    def excluir(e):
        page.pop_dialog()
        ao_excluir(campo_pergunta.value or "", campo_resposta.value or "")

    return ft.AlertDialog(
        title=ft.Text("Editar flashcard"),
        content=ft.Column(
            tight=True,
            spacing=8,
            controls=[campo_pergunta, campo_resposta, erro],
        ),
        actions=[
            ft.TextButton(
                "Excluir",
                on_click=excluir,
                style=ft.ButtonStyle(color=ft.Colors.ERROR),
            ),
            ft.Row(
                tight=True,
                spacing=8,
                controls=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.FilledButton("Salvar", on_click=salvar),
                ],
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def dialog_excluir_flashcard(
    page: ft.Page, pergunta: str, ao_excluir, ao_cancelar=None
) -> ft.AlertDialog:
    erro = ft.Text("", color=ft.Colors.ERROR, size=12)

    def excluir(e):
        try:
            ao_excluir()
        except ValueError as falha:
            erro.value = str(falha)
            erro.visible = True
            erro.update()
            return
        page.pop_dialog()

    def cancelar(e):
        page.pop_dialog()
        if ao_cancelar:
            ao_cancelar()

    return ft.AlertDialog(
        title=ft.Text("Excluir pergunta?"),
        content=ft.Column(
            tight=True,
            spacing=8,
            controls=[
                ft.Text(pergunta, weight=ft.FontWeight.W_600),
                ft.Text("A resposta dessa pergunta também será apagada."),
                erro,
            ],
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.FilledButton(
                "Excluir",
                on_click=excluir,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.ERROR,
                    color=ft.Colors.ON_ERROR,
                ),
            ),
        ],
    )
