import flet as ft


def dialog_nome_materia(
    page: ft.Page, titulo: str, valor: str, ao_salvar
) -> ft.AlertDialog:
    campo = ft.TextField(label="Nome da matéria", value=valor, autofocus=True)
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


def dialog_criar_materia(page: ft.Page, ao_criar) -> ft.AlertDialog:
    return dialog_nome_materia(page, "Criar Matéria", "", ao_criar)


def dialog_editar_materia(
    page: ft.Page, nome_atual: str, ao_renomear
) -> ft.AlertDialog:
    return dialog_nome_materia(page, "Editar nome", nome_atual, ao_renomear)


def dialog_excluir_materia(page: ft.Page, nome: str, ao_excluir) -> ft.AlertDialog:
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
                ft.Text("Os flashcards dessa matéria também serão apagados."),
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


def dialog_selecionar_materia(
    page: ft.Page,
    titulo: str,
    materias: list[str],
    materia_atual: str | None,
    ao_escolher,
    ao_esvaziar=None,
) -> ft.AlertDialog:
    def escolher(nome: str):
        ao_escolher(nome)
        page.pop_dialog()

    def esvaziar(e):
        if ao_esvaziar:
            ao_esvaziar()
        page.pop_dialog()

    def fechar(e):
        page.pop_dialog()

    if materias:
        opcoes = [
            ft.ListTile(
                title=ft.Text(nome),
                on_click=(lambda e, n=nome: escolher(n)),
            )
            for nome in materias
        ]
    else:
        opcoes = [ft.Text("Nenhuma matéria criada ainda.")]

    acoes = []
    if materia_atual:
        acoes.append(
            ft.TextButton(
                "Esvaziar",
                on_click=esvaziar,
                style=ft.ButtonStyle(color=ft.Colors.ERROR),
            )
        )
    acoes.append(ft.TextButton("Fechar", on_click=fechar))

    return ft.AlertDialog(
        title=ft.Text(titulo),
        content=ft.Column(
            tight=True,
            controls=opcoes,
        ),
        actions=acoes,
        actions_alignment=(
            ft.MainAxisAlignment.SPACE_BETWEEN if materia_atual else None
        ),
    )
