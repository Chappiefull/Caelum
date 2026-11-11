import random

import flet as ft

from tela_flashcard import backend, barra, campos, dialogos, lista

ROUTE = "/flashcard"
ROTA_EXECUCAO = "/execucao"


def estilo_texto_chip(selecionado: bool) -> ft.TextStyle | None:
    if selecionado:
        return ft.TextStyle(color=ft.Colors.PRIMARY_CONTAINER)
    return None


def view(page: ft.Page, **params) -> ft.View:
    materia = params.get("materia", "")
    nome = params.get("flashcard", "")
    estado = {
        "flashcards": backend.listar_flashcards(materia, nome),
        "busca": "",
        "aleatorio": False,
        "invertido": False,
    }

    coluna = ft.Column(
        spacing=lista.ESPACAMENTO,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        margin=ft.Margin.only(bottom=100),
    )

    def itens() -> list[tuple[str, str]]:
        visiveis = lista.filtrar(
            estado["flashcards"], estado["busca"], estado["invertido"]
        )
        if estado["aleatorio"]:
            visiveis = random.sample(visiveis, len(visiveis))
        return visiveis

    def renderizar() -> None:
        coluna.controls = [
            lista.campos_flashcards(
                par,
                estado["invertido"],
                editar,
            )
            for par in lista.fatiar(itens(), 2)
        ]

    def recarregar() -> None:
        estado["flashcards"] = backend.listar_flashcards(materia, nome)
        renderizar()
        coluna.update()

    def salvar(e=None) -> None:
        controles = area_campos.data
        pergunta = controles["pergunta"].value or ""
        resposta = controles["resposta"].value or ""
        try:
            backend.criar_flashcard(materia, nome, pergunta, resposta)
        except ValueError as falha:
            controles["erro"].value = str(falha)
            controles["erro"].visible = True
            controles["erro"].update()
            return
        controles["erro"].value = ""
        controles["erro"].visible = False
        controles["pergunta"].value = ""
        controles["resposta"].value = ""
        for controle in controles.values():
            controle.update()
        recarregar()

    def editar(
        pergunta: str,
        pergunta_inicial: str | None = None,
        resposta_inicial: str | None = None,
    ) -> None:
        resposta = dict(estado["flashcards"]).get(pergunta, "")
        page.show_dialog(
            dialogos.dialog_editar_flashcard(
                page,
                pergunta if pergunta_inicial is None else pergunta_inicial,
                resposta if resposta_inicial is None else resposta_inicial,
                lambda nova_pergunta, nova_resposta: salvar_edicao(
                    pergunta, nova_pergunta, nova_resposta
                ),
                lambda nova_pergunta, nova_resposta: confirmar_exclusao(
                    pergunta, nova_pergunta, nova_resposta
                ),
            )
        )

    def salvar_edicao(antiga: str, pergunta: str, resposta: str) -> None:
        backend.editar_flashcard(materia, nome, antiga, pergunta, resposta)
        recarregar()

    def confirmar_exclusao(
        pergunta: str,
        pergunta_inicial: str | None = None,
        resposta_inicial: str | None = None,
    ) -> None:
        ao_cancelar = None
        if pergunta_inicial is not None and resposta_inicial is not None:
            ao_cancelar = lambda: editar(
                pergunta, pergunta_inicial, resposta_inicial
            )
        page.show_dialog(
            dialogos.dialog_excluir_flashcard(
                page,
                pergunta,
                lambda: excluir(pergunta),
                ao_cancelar=ao_cancelar,
            )
        )

    def excluir(pergunta: str) -> None:
        backend.excluir_flashcard(materia, nome, pergunta)
        recarregar()

    def buscar(e):
        estado["busca"] = e.control.value or ""
        renderizar()
        coluna.update()

    def aleatorio(e):
        estado["aleatorio"] = not estado["aleatorio"]
        e.control.selected = estado["aleatorio"]
        e.control.label_text_style = estilo_texto_chip(estado["aleatorio"])
        e.control.update()
        renderizar()
        coluna.update()

    def inverter(e):
        estado["invertido"] = not estado["invertido"]
        e.control.selected = estado["invertido"]
        e.control.label_text_style = estilo_texto_chip(estado["invertido"])
        e.control.update()
        renderizar()
        coluna.update()

    def executar(e):
        visiveis = itens()
        if not visiveis:
            return
        indice = estado["flashcards"].index(visiveis[0])
        extras = {"invertido": "1"} if estado["invertido"] else {}
        page.navigate(
            ROTA_EXECUCAO,
            materia=materia,
            flashcard=nome,
            indice=indice,
            origem="flashcard",
            **extras,
        )

    area_campos = campos.campos_de_texto()

    renderizar()

    return ft.View(
        route=ROUTE,
        padding=15,
        appbar=ft.AppBar(title=ft.Text(nome)),
        controls=[
            area_campos,
            barra.barra(buscar, aleatorio, inverter, executar, salvar),
            ft.Divider(thickness=0.1),
            coluna,
        ],
    )


def main(page: ft.Page) -> None:
    page.title = "Flashcards"
    page.views.append(view(page, materia="Biologia", flashcard="ciclo celular"))
    page.update()


if __name__ == "__main__":
    ft.run(main)
