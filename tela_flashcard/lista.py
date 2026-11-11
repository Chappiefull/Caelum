import flet as ft

ESPACAMENTO = 12


def fatiar(lst: list, n: int) -> list[list]:
    return [lst[i: i + n] for i in range(0, len(lst), n)]


def filtrar(
    lst: list[tuple[str, str]], termo: str, buscar_respostas: bool = False
) -> list[tuple[str, str]]:
    if not termo:
        return list(lst)
    alvo = termo.strip().lower()
    if not alvo:
        return list(lst)
    if buscar_respostas:
        return [(p, r) for p, r in lst if alvo in r.lower()]
    return [(p, r) for p, r in lst if alvo in p.lower()]


def celula(
    pergunta: str,
    resposta: str,
    exibir_resposta: bool = False,
    on_editar=None,
) -> ft.Container:
    texto = resposta if exibir_resposta else pergunta

    return ft.Container(
        content=ft.Text(
            texto,
            size=12,
            weight=ft.FontWeight.W_600,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
            text_align=ft.TextAlign.CENTER,
        ),
        height=60,
        alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border_radius=8,
        expand=True,
        on_click=(lambda e: on_editar(pergunta)) if on_editar else None,
    )


def campos_flashcards(
    pares: list[tuple[str, str]],
    exibir_respostas: bool = False,
    on_editar=None,
) -> ft.Row:
    controles = [
        celula(pergunta, resposta, exibir_respostas, on_editar)
        for pergunta, resposta in pares
    ]
    return ft.Row(spacing=ESPACAMENTO, controls=controles)
