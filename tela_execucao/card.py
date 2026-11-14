import flet as ft


def card_pergunta_resposta(texto: ft.Text) -> ft.Container:
    return ft.Container(
        content=texto,
        expand=True,
        margin=15,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        border_radius=10,
    )
