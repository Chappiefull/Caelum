import flet as ft

LARGURA = 120
ALTURA = 200


def flashcard(
    nome: str,
    total: int,
    on_play=None,
    on_click=None,
    on_editar=None,
    on_excluir=None,
) -> ft.ContextMenu:
    acoes = [on_editar, on_excluir]

    def selecionar(e):
        if e.item_index is not None and 0 <= e.item_index < len(acoes):
            acao = acoes[e.item_index]
            if acao:
                acao(e)

    return ft.ContextMenu(
        content=ft.Container(
            content=ft.Stack(
                fit=ft.StackFit.EXPAND,
                controls=[
                    ft.Text(
                        str(total),
                        size=15,
                        weight=ft.FontWeight.W_400,
                        align=ft.Alignment.TOP_LEFT,
                        margin=ft.Margin.only(left=5, top=2),
                    ),
                    ft.FilledButton(
                        icon=ft.Icons.PLAY_ARROW,
                        align=ft.Alignment.TOP_RIGHT,
                        height=25,
                        width=25,
                        on_click=on_play,
                        style=ft.ButtonStyle(
                            alignment=ft.Alignment.CENTER,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.Padding.only(top=5, bottom=5, left=4),
                        ),
                        margin=ft.Margin.all(2),
                    ),
                    ft.Text(
                        nome,
                        size=18,
                        weight=ft.FontWeight.W_500,
                        align=ft.Alignment.BOTTOM_LEFT,
                        margin=ft.Margin.only(left=5),
                        max_lines=3,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
            ),
            width=LARGURA,
            height=ALTURA,
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            on_click=on_click,
        ),
        secondary_items=[
            ft.PopupMenuItem(content="Editar nome"),
            ft.PopupMenuItem(content="Excluir"),
        ],
        on_select=selecionar,
    )
