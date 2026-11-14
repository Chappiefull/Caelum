import flet as ft

from tela_execucao import backend, card

ROUTE = "/execucao"
ROTA_MATERIA = "/materia"
ROTA_FLASHCARD = "/flashcard"


def view(page: ft.Page, **params) -> ft.View:
    materia = params.get("materia", "")
    nome = params.get("flashcard", "")
    indice = int(params.get("indice", 0))
    invertido = params.get("invertido") == "1"
    origem = params.get("origem", "materia")

    pares = backend.listar_flashcards(materia, nome)
    if not pares:
        pares = [("", "")]
    indice = max(0, min(indice, len(pares) - 1))
    fila = pares[indice:] + pares[:indice]
    virada = False

    texto = ft.Text(
        "",
        weight=ft.FontWeight.W_500,
        size=18,
        align=ft.Alignment.CENTER,
    )
    cartao = card.card_pergunta_resposta(texto)

    def conteudo() -> str:
        pergunta, resposta = fila[0]
        frente, verso = (resposta, pergunta) if invertido else (pergunta, resposta)
        return verso if virada else frente

    def voltar() -> None:
        if origem == "flashcard":
            page.navigate(ROTA_FLASHCARD, materia=materia, flashcard=nome)
        else:
            page.navigate(ROTA_MATERIA, materia=materia)

    def virar(e):
        nonlocal virada
        virada = not virada
        renderizar()

    def errei(e):
        nonlocal virada
        fila.append(fila.pop(0))
        virada = False
        renderizar()

    def acertei(e):
        nonlocal virada
        fila.pop(0)
        virada = False
        if not fila:
            voltar()
            return
        renderizar()

    botao_errei = ft.FilledButton(
        content="errei",
        height=40,
        visible=False,
        on_click=errei,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ERROR,
            color=ft.Colors.ON_ERROR,
        ),
    )
    botao_virar = ft.FilledButton("Virar flashcard", height=40, on_click=virar)
    botao_acertei = ft.FilledButton(
        content="acertei",
        height=40,
        visible=False,
        on_click=acertei,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
        ),
    )

    botoes = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
        controls=[botao_errei, botao_virar, botao_acertei],
    )

    def renderizar() -> None:
        texto.value = conteudo()
        botao_errei.visible = virada
        botao_acertei.visible = virada
        texto.update()
        botoes.update()

    texto.value = conteudo()

    return ft.View(
        route=ROUTE,
        padding=15,
        appbar=ft.AppBar(title=ft.Text(nome)),
        controls=[
            cartao,
            botoes,
        ],
    )


def main(page: ft.Page) -> None:
    page.title = "Execução"
    page.views.append(
        view(page, materia="Biologia", flashcard="ciclo celular", indice=0)
    )
    page.update()


if __name__ == "__main__":
    ft.run(main)
