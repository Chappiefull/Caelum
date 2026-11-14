import armazenamento

def listar_materias():
    """Retorna uma lista de strings com os nomes de todas as matérias cadastradas."""
    dados = armazenamento.ler_json("materias.json")
    if not dados:
        return []
    return dados.get("materias", [])

def adicionar_materia(nome_materia):
    """Adiciona uma nova matéria se ela não existir e cria a pasta física dela."""
    nome_materia = nome_materia.strip()
    if not nome_materia:
        return False

    dados = armazenamento.ler_json("materias.json") or {"materias": []}

    if nome_materia in dados["materias"]:
        return False

    dados["materias"].append(nome_materia)
    armazenamento.salvar_json("materias.json", dados)
    armazenamento.criar_pasta(nome_materia)
    return True

def renomear_materia(nome_antigo, nome_novo):
    """Altera o nome de uma matéria e renomeia sua pasta física correspondente."""
    nome_novo = nome_novo.strip()
    if not nome_novo or nome_antigo == nome_novo:
        return False

    dados = armazenamento.ler_json("materias.json")
    if not dados or nome_antigo not in dados.get("materias", []):
        return False

    if nome_novo in dados["materias"]:
        return False

    index = dados["materias"].index(nome_antigo)
    dados["materias"][index] = nome_novo
    armazenamento.salvar_json("materias.json", dados)
    armazenamento.renomear_pasta(nome_antigo, nome_novo)
    return True

def excluir_materia(nome_materia):
    """Remove a matéria da lista e deleta permanentemente sua pasta e arquivos."""
    dados = armazenamento.ler_json("materias.json")
    if not dados or nome_materia not in dados.get("materias", []):
        return False

    dados["materias"].remove(nome_materia)
    armazenamento.salvar_json("materias.json", dados)
    armazenamento.excluir_pasta(nome_materia)
    return True

def obter_agenda():
    """Retorna o dicionário representando a grade horária/agenda de estudos (7 colunas x 3 períodos)."""
    agenda = armazenamento.ler_json("agenda.json")
    if not agenda:
        # Inicializa uma agenda vazia padronizada
        agenda = {str(dia): {str(periodo): "" for periodo in range(3)} for dia in range(7)}
    return agenda

def salvar_slot_agenda(dia, periodo, nome_materia):
    """Vincula ou desvincula uma matéria a um determinado slot da agenda."""
    agenda = obter_agenda()
    agenda[str(dia)][str(periodo)] = nome_materia.strip()
    return armazenamento.salvar_json("agenda.json", agenda)
