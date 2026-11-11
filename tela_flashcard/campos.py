import flet as ft

ALTURA_CAMPO = 5


def campos_de_texto() -> ft.Column:
    pergunta = ft.TextField(
        label="Pergunta",
        col={"xs": 12, "sm": 6},
        multiline=True,
        min_lines=ALTURA_CAMPO,
        max_lines=ALTURA_CAMPO,
        filled=True,
        border_radius=10,
    )
    resposta = ft.TextField(
        label="Resposta",
        col={"xs": 12, "sm": 6},
        multiline=True,
        min_lines=ALTURA_CAMPO,
        max_lines=ALTURA_CAMPO,
        filled=True,
        border_radius=10,
    )
    erro = ft.Text("", color=ft.Colors.ERROR, size=12, visible=False)

    coluna = ft.Column(
        spacing=8,
        controls=[
            ft.ResponsiveRow(controls=[pergunta, resposta]),
            erro,
        ],
    )
    coluna.data = {"pergunta": pergunta, "resposta": resposta, "erro": erro}
    return coluna
