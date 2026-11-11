import flet as ft

from cronometro import Cronometro, formatar


def timer(nome_materia: str, crono: Cronometro) -> ft.ContextMenu:
    nome = ft.Text(
        nome_materia,
        size=20,
        weight=ft.FontWeight.W_400,
        align=ft.Alignment.TOP_CENTER,
        margin=ft.Margin.only(top=9),
    )
    texto = ft.Text(
        formatar(crono.segundos),
        size=50,
        weight=ft.FontWeight.W_500,
        font_family="JetBrainsMono NFM",
        align=ft.Alignment.CENTER,
    )
    cartao = ft.Container(
        content=ft.Stack(
            fit=ft.StackFit.EXPAND,
            controls=[nome, texto],
        ),
        height=300,
        width=float("inf"),
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        border_radius=15,
        on_click=crono.alternar,
    )
    crono.cartao = cartao
    crono.nome = nome
    crono.texto = texto
    if crono.rodando:
        cartao.bgcolor = ft.Colors.PRIMARY
        nome.color = ft.Colors.ON_PRIMARY
        texto.color = ft.Colors.ON_PRIMARY
    return ft.ContextMenu(
        content=cartao,
        expand=True,
        secondary_items=[ft.PopupMenuItem(content="Resetar")],
        on_select=lambda e: crono.resetar(),
    )
