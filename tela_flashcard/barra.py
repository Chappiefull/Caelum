import flet as ft


def barra(
    on_busca, on_aleatorio, on_inverter, on_play, on_adicionar
) -> ft.Container:
    return ft.Container(
        ft.Row(
            controls=[
                ft.Container(
                    content=ft.TextField(
                        hint_text="Pesquisar",
                        border_radius=10,
                        on_change=on_busca,
                    ),
                    expand=True,
                    align=ft.Alignment(-1, 0),
                    margin=ft.Margin.only(left=5),
                ),
                ft.FilledButton(
                    "Adicionar flashcard",
                    width=200,
                    height=35,
                    align=ft.Alignment.CENTER,
                    on_click=on_adicionar,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Chip(
                                label="aleatório",
                                selected_color=ft.Colors.ON_PRIMARY_CONTAINER,
                                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                                border_side=ft.BorderSide.none(),
                                show_checkmark=False,
                                on_select=on_aleatorio,
                            ),
                            ft.Chip(
                                label="inverter",
                                selected_color=ft.Colors.ON_PRIMARY_CONTAINER,
                                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                                border_side=ft.BorderSide.none(),
                                show_checkmark=False,
                                on_select=on_inverter,
                            ),
                            ft.FilledButton(
                                content="",
                                icon=ft.Icons.PLAY_ARROW,
                                height=40,
                                on_click=on_play,
                                style=ft.ButtonStyle(
                                    padding=ft.Padding.only(left=5)
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    expand=True,
                    align=ft.Alignment(1, 0),
                    margin=ft.Margin.only(right=5),
                ),
            ],
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border_radius=20,
        padding=10,
    )
