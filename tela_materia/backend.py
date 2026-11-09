import armazenamento

EXTENSAO = ".json"


def listar_flashcards(materia: str) -> list[str]:
    return armazenamento.listar_flashcards(materia)


def contar_perguntas(materia: str, nome: str) -> int:
    return len(armazenamento.ler_flashcard(materia, nome))


def _validar_nome(materia: str, nome: str) -> str:
    nome = nome.strip()
    if not nome:
        raise ValueError("O nome do baralho não pode ficar vazio")
    if "/" in nome or "\\" in nome:
        raise ValueError("O nome do baralho não pode conter /")
    if nome in (".", ".."):
        raise ValueError("O nome do baralho é inválido")
    if nome.lower().endswith(EXTENSAO):
        nome = nome[: -len(EXTENSAO)]
    if not nome:
        raise ValueError("O nome do baralho não pode ficar vazio")
    if nome in listar_flashcards(materia):
        raise ValueError(f"O baralho “{nome}” já existe")
    return nome


def criar_flashcard(materia: str, nome: str) -> str:
    nome = _validar_nome(materia, nome)
    armazenamento.criar_flashcard(materia, nome)
    return nome


def renomear_flashcard(materia: str, antigo: str, novo: str) -> str:
    novo = novo.strip()
    if novo.lower().endswith(EXTENSAO):
        novo = novo[: -len(EXTENSAO)]
    if novo == antigo:
        return antigo
    if antigo not in listar_flashcards(materia):
        raise ValueError(f"O baralho “{antigo}” não existe")
    novo = _validar_nome(materia, novo)
    armazenamento.renomear_flashcard(materia, antigo, novo)
    return novo


def excluir_flashcard(materia: str, nome: str) -> None:
    if nome not in listar_flashcards(materia):
        raise ValueError(f"O baralho “{nome}” não existe")
    armazenamento.excluir_flashcard(materia, nome)
