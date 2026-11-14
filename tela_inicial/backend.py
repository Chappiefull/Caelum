import armazenamento

DIAS = ["seg", "ter", "quar", "quin", "sex", "sab", "dom"]
NOMES_DIAS = {
    "seg": "Segunda",
    "ter": "Terça",
    "quar": "Quarta",
    "quin": "Quinta",
    "sex": "Sexta",
    "sab": "Sábado",
    "dom": "Domingo",
}
PERIODOS = ["dia", "tarde", "noite"]
NOME_RESERVADO = "agenda"


def listar_materias() -> list[str]:
    return armazenamento.listar_pastas_materia()


def _validar_nome(nome: str) -> str:
    nome = nome.strip()
    if not nome:
        raise ValueError("O nome da matéria não pode ficar vazio")
    if "/" in nome or "\\" in nome:
        raise ValueError("O nome da matéria não pode conter /")
    if nome.lower() == NOME_RESERVADO:
        raise ValueError(f"O nome “{NOME_RESERVADO}” é reservado")
    if nome in listar_materias():
        raise ValueError(f"A matéria “{nome}” já existe")
    return nome


def criar_materia(nome: str) -> str:
    nome = _validar_nome(nome)
    armazenamento.criar_pasta_materia(nome)
    return nome


def renomear_materia(antiga: str, nova: str) -> str:
    nova = nova.strip()
    if nova == antiga:
        return antiga
    if antiga not in listar_materias():
        raise ValueError(f"A matéria “{antiga}” não existe")
    nova = _validar_nome(nova)
    armazenamento.renomear_pasta_materia(antiga, nova)
    agenda = armazenamento.ler_agenda()
    armazenamento.gravar_agenda(
        {slot: nova if nome == antiga else nome for slot, nome in agenda.items()}
    )
    return nova


def excluir_materia(nome: str) -> None:
    if nome not in listar_materias():
        raise ValueError(f"A matéria “{nome}” não existe")
    armazenamento.excluir_pasta_materia(nome)
    agenda = armazenamento.ler_agenda()
    armazenamento.gravar_agenda(
        {slot: materia for slot, materia in agenda.items() if materia != nome}
    )


def listar_agenda() -> dict[str, str]:
    """Agenda sem as matérias que não existem mais como pasta em `data/`."""
    existentes = set(listar_materias())
    return {
        slot: nome
        for slot, nome in armazenamento.ler_agenda().items()
        if nome in existentes
    }


def materia_do_slot(dia: str, periodo: str) -> str | None:
    return listar_agenda().get(f"{dia}/{periodo}")


def agendar(dia: str, periodo: str, materia: str) -> None:
    agenda = listar_agenda()
    agenda[f"{dia}/{periodo}"] = materia
    armazenamento.gravar_agenda(agenda)


def desagendar(dia: str, periodo: str) -> None:
    agenda = listar_agenda()
    agenda.pop(f"{dia}/{periodo}", None)
    armazenamento.gravar_agenda(agenda)
