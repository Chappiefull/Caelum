import json
import locale
import shutil
from pathlib import Path

try:
    locale.setlocale(locale.LC_COLLATE, "pt_BR.UTF-8")
except locale.Error:
    pass

RAIZ = Path(__file__).resolve().parent
DATA = RAIZ / "data"
ARQUIVO_AGENDA = DATA / "agenda.json"
EXTENSAO = ".json"


def ordenar(nomes: list[str]) -> list[str]:
    return sorted(nomes, key=locale.strxfrm)


def caminho_materia(nome: str) -> Path:
    return DATA / nome


def caminho_flashcard(materia: str, nome: str) -> Path:
    return caminho_materia(materia) / f"{nome}{EXTENSAO}"


def listar_pastas_materia() -> list[str]:
    if not DATA.exists():
        return []
    return ordenar(pasta.name for pasta in DATA.iterdir() if pasta.is_dir())


def criar_pasta_materia(nome: str) -> Path:
    pasta = caminho_materia(nome)
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def renomear_pasta_materia(antiga: str, nova: str) -> Path:
    destino = caminho_materia(nova)
    caminho_materia(antiga).rename(destino)
    return destino


def excluir_pasta_materia(nome: str) -> None:
    shutil.rmtree(caminho_materia(nome), ignore_errors=True)


def listar_flashcards(materia: str) -> list[str]:
    pasta = caminho_materia(materia)
    if not pasta.exists():
        return []
    return ordenar(
        arquivo.stem
        for arquivo in pasta.iterdir()
        if arquivo.is_file() and arquivo.suffix == EXTENSAO
    )


def criar_flashcard(materia: str, nome: str) -> Path:
    arquivo = caminho_flashcard(materia, nome)
    gravar_json(arquivo, {})
    return arquivo


def renomear_flashcard(materia: str, antigo: str, novo: str) -> Path:
    destino = caminho_flashcard(materia, novo)
    caminho_flashcard(materia, antigo).rename(destino)
    return destino


def excluir_flashcard(materia: str, nome: str) -> None:
    caminho_flashcard(materia, nome).unlink(missing_ok=True)


def ler_flashcard(materia: str, nome: str) -> dict[str, str]:
    return ler_json(caminho_flashcard(materia, nome))


def gravar_flashcard(materia: str, nome: str, flashcards: dict[str, str]) -> None:
    gravar_json(caminho_flashcard(materia, nome), flashcards)


def ler_json(arquivo: Path) -> dict:
    if not arquivo.exists():
        return {}
    with arquivo.open("r", encoding="utf-8") as f:
        return json.load(f)


def gravar_json(arquivo: Path, dados: dict) -> None:
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    with arquivo.open("w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def ler_agenda() -> dict[str, str]:
    return ler_json(ARQUIVO_AGENDA)


def gravar_agenda(agenda: dict[str, str]) -> None:
    gravar_json(ARQUIVO_AGENDA, agenda)
