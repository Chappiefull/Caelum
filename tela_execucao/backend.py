import armazenamento


def listar_flashcards(materia: str, nome: str) -> list[tuple[str, str]]:
    return list(armazenamento.ler_flashcard(materia, nome).items())


def obter_flashcard(materia: str, nome: str, indice: int) -> tuple[str, str]:
    flashcards = listar_flashcards(materia, nome)
    return flashcards[indice]
