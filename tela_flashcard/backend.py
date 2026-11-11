import armazenamento


def listar_flashcards(materia: str, nome: str) -> list[tuple[str, str]]:
    return list(armazenamento.ler_flashcard(materia, nome).items())


def _validar_campos(pergunta: str, resposta: str) -> tuple[str, str]:
    pergunta = pergunta.strip()
    resposta = resposta.strip()
    if not pergunta and not resposta:
        raise ValueError("A pergunta e a resposta não podem ficar vazias")
    if not pergunta:
        raise ValueError("A pergunta não pode ficar vazia")
    if not resposta:
        raise ValueError("A resposta não pode ficar vazia")
    return pergunta, resposta


def criar_flashcard(materia: str, nome: str, pergunta: str, resposta: str) -> None:
    pergunta, resposta = _validar_campos(pergunta, resposta)

    flashcards = armazenamento.ler_flashcard(materia, nome)
    if pergunta in flashcards:
        raise ValueError("Essa pergunta já existe")
    flashcards[pergunta] = resposta
    armazenamento.gravar_flashcard(materia, nome, flashcards)


def editar_flashcard(
    materia: str,
    nome: str,
    pergunta_antiga: str,
    pergunta: str,
    resposta: str,
) -> None:
    pergunta, resposta = _validar_campos(pergunta, resposta)

    flashcards = armazenamento.ler_flashcard(materia, nome)
    if pergunta_antiga not in flashcards:
        raise ValueError("Essa pergunta não existe")

    if pergunta == pergunta_antiga:
        flashcards[pergunta] = resposta
    else:
        if pergunta in flashcards:
            raise ValueError("Essa pergunta já existe")
        editado = {}
        for chave, valor in flashcards.items():
            if chave == pergunta_antiga:
                editado[pergunta] = resposta
            else:
                editado[chave] = valor
        flashcards = editado

    armazenamento.gravar_flashcard(materia, nome, flashcards)


def excluir_flashcard(materia: str, nome: str, pergunta: str) -> None:
    flashcards = armazenamento.ler_flashcard(materia, nome)
    if pergunta not in flashcards:
        raise ValueError("Essa pergunta não existe")
    del flashcards[pergunta]
    armazenamento.gravar_flashcard(materia, nome, flashcards)
