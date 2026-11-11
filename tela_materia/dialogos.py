import flet as ft


def dialog_nome_flashcard(
    page: ft.Page, titulo: str, valor: str, ao_salvar
) -> ft.AlertDialog:
    campo = ft.TextField(label="Nome do baralho", value=valor, autofocus=True)
    erro = ft.Text("", color=ft.Colors.ERROR, size=12)

    def salvar(e):
        try:
            ao_salvar(campo.value or "")
        except ValueError as falha:
            erro.value = str(falha)
            erro.visible = True
            erro.update()
            return
        page.pop_dialog()

    def cancelar(e):
        page.pop_dialog()

    return ft.AlertDialog(
        title=ft.Text(titulo),
        content=ft.Column(
            tight=True,
            controls=[campo, erro],
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.FilledButton("Salvar", on_click=salvar),
        ],
    )


def dialog_criar_flashcard(page: ft.Page, ao_criar) -> ft.AlertDialog:
    return dialog_nome_flashcard(page, "Criar baralho", "", ao_criar)


def dialog_editar_flashcard(
    page: ft.Page, nome_atual: str, ao_renomear
) -> ft.AlertDialog:
    return dialog_nome_flashcard(page, "Editar nome", nome_atual, ao_renomear)


def dialog_excluir_flashcard(
    page: ft.Page, nome: str, ao_excluir
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

    return ft.AlertDialog(
        title=ft.Text(f"Excluir “{nome}”?"),
        content=ft.Column(
            tight=True,
            controls=[
                ft.Text("As perguntas desse baralho também serão apagadas."),
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
