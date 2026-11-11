import flet as ft


def materia(
    nome: str, on_click=None, on_editar=None, on_excluir=None
) -> ft.Row:
    acoes = [on_editar, on_excluir]

    def selecionar(e):
        if e.item_index is not None and 0 <= e.item_index < len(acoes):
            acao = acoes[e.item_index]
            if acao:
                acao(e)

    return ft.Row(
        controls=[
            ft.ContextMenu(
                content=ft.Container(
                    content=ft.Text(nome, size=20, weight=ft.FontWeight.W_300),
                    border=ft.Border.all(width=1.0, color=ft.Colors.OUTLINE),
                    height=80,
                    width=float("inf"),
                    border_radius=9,
                    alignment=ft.Alignment.CENTER_LEFT,
                    padding=10,
                    on_click=on_click,
                ),
                expand=True,
                secondary_items=[
                    ft.PopupMenuItem(content="Editar nome"),
                    ft.PopupMenuItem(content="Excluir"),
                ],
                on_select=selecionar,
            )
        ]
    )
