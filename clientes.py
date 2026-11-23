from dados import salvar_dados, limpar_texto_numerico, confirmar_acao

OPCOES_SEXO = {
    "1": "Masculino",
    "2": "Feminino",
    "3": "Outro / Prefiro não informar"
}


def buscar_cliente_por_cpf(dados, cpf):
    """Retorna o dicionário do cliente pelo CPF ou None se não encontrar."""
    cpf_limpo = limpar_texto_numerico(cpf)
    for cliente in dados["clientes"]:
        if cliente["cpf"] == cpf_limpo:
            return cliente
    return None


def selecionar_cliente_interativo(dados, titulo_acao="SELECIONAR CLIENTE"):
    """Permite localizar um cliente pelo CPF ou pelo Nome (com seleção caso haja homônimos)."""
    termo = input("Digite o CPF ou o nome do cliente: ").strip()
    if not termo:
        print("\n[ERRO] Digite um termo para pesquisa.")
        return None

    termo_numerico = limpar_texto_numerico(termo)
    encontrados = []

    for cliente in dados["clientes"]:
        if (termo_numerico and termo_numerico == cliente["cpf"]) or (termo.lower() in cliente["nome"].lower()):
            encontrados.append(cliente)

    if not encontrados:
        print("\n[AVISO] Nenhum cliente encontrado com os dados informados.")
        return None

    if len(encontrados) == 1:
        return encontrados[0]

    print(f"\nForam encontrados {len(encontrados)} clientes para '{termo}':")
    print("-" * 55)
    for idx, c in enumerate(encontrados, start=1):
        print(f"  {idx} - {c['nome']} | CPF: {c['cpf']} | [{c['status']}]")
    print("-" * 55)

    try:
        escolha = int(input("Escolha o número do cliente desejado: ").strip())
        if 1 <= escolha <= len(encontrados):
            return encontrados[escolha - 1]
        else:
            print("\n[ERRO] Número fora da lista.")
            return None
    except ValueError:
        print("\n[ERRO] Entrada inválida! Digite o número correspondente ao cliente.")
        return None


def cadastrar_cliente(dados):
    print("\n" + "=" * 45)
    print("           CADASTRAR NOVO CLIENTE")
    print("=" * 45)

    cpf_input = input("CPF (somente números ou com pontuação): ").strip()
    cpf = limpar_texto_numerico(cpf_input)

    if len(cpf) != 11:
        print("\n[ERRO] CPF inválido! Deve conter exatamente 11 dígitos numéricos.")
        return

    if buscar_cliente_por_cpf(dados, cpf) is not None:
        print("\n[ERRO] Já existe um cliente cadastrado com este CPF.")
        return

    nome = input("Nome completo: ").strip()
    if not nome:
        print("\n[ERRO] O nome completo é obrigatório.")
        return

    print("\nSexo do cliente:")
    for codigo, descricao in OPCOES_SEXO.items():
        print(f"  {codigo} - {descricao}")
    opcao_sexo = input("Escolha uma opção: ").strip()
    if opcao_sexo not in OPCOES_SEXO:
        print("\n[ERRO] Opção de sexo inválida.")
        return
    sexo = OPCOES_SEXO[opcao_sexo]

    telefone = input("Telefone (com DDD): ").strip()
    if not telefone:
        print("\n[ERRO] O telefone é obrigatório.")
        return

    endereco = input("Endereço completo: ").strip()
    if not endereco:
        print("\n[ERRO] O endereço é obrigatório.")
        return

    novo_cliente = {
        "cpf": cpf,
        "nome": nome,
        "sexo": sexo,
        "telefone": telefone,
        "endereco": endereco,
        "status": "Ativo"
    }

    dados["clientes"].append(novo_cliente)
    salvar_dados(dados)
    print(f"\n[SUCESSO] Cliente '{nome}' cadastrado com sucesso!")


def listar_clientes(dados):
    print("\n" + "=" * 65)
    print("                      LISTA DE CLIENTES")
    print("=" * 65)

    if not dados["clientes"]:
        print("Nenhum cliente cadastrado no sistema.")
        return

    for cliente in dados["clientes"]:
        sexo = cliente.get("sexo", "Não informado")
        print(f"CPF: {cliente['cpf']} | Nome: {cliente['nome']} | Sexo: {sexo} | [{cliente['status']}]")
        print(f"Telefone: {cliente['telefone']} | Endereço: {cliente['endereco']}")
        print("-" * 65)


def consultar_cliente(dados):
    print("\n" + "=" * 45)
    print("             CONSULTAR CLIENTE")
    print("=" * 45)

    termo = input("Digite o CPF ou parte do nome do cliente: ").strip()
    if not termo:
        print("\n[ERRO] Digite um termo para pesquisa.")
        return

    termo_numerico = limpar_texto_numerico(termo)
    encontrados = []

    for cliente in dados["clientes"]:
        if (termo_numerico and termo_numerico == cliente["cpf"]) or (termo.lower() in cliente["nome"].lower()):
            encontrados.append(cliente)

    if not encontrados:
        print("\n[AVISO] Nenhum cliente encontrado com os dados informados.")
        return

    print(f"\n{len(encontrados)} registro(s) encontrado(s):")
    print("-" * 65)
    for c in encontrados:
        sexo = c.get("sexo", "Não informado")
        print(f"Nome:     {c['nome']} ({c['status']})")
        print(f"CPF:      {c['cpf']} | Sexo: {sexo}")
        print(f"Telefone: {c['telefone']}")
        print(f"Endereço: {c['endereco']}")
        print("-" * 65)


def alterar_cliente(dados):
    print("\n" + "=" * 45)
    print("         ALTERAR DADOS DO CLIENTE")
    print("=" * 45)

    cliente = selecionar_cliente_interativo(dados)
    if cliente is None:
        return

    if cliente["status"] == "Cancelado":
        print("\n[ERRO] Não é possível alterar um cadastro cancelado.")
        return

    sexo_atual = cliente.get("sexo", "Não informado")
    print(f"\nEditando cliente: {cliente['nome']} (CPF: {cliente['cpf']})")
    print("(Deixe em branco e pressione ENTER para manter o valor atual)\n")

    novo_nome = input(f"Nome atual [{cliente['nome']}]: ").strip()

    print(f"Sexo atual [{sexo_atual}] (1-Masculino | 2-Feminino | 3-Outro | ENTER para manter):")
    opcao_sexo = input("Novo sexo: ").strip()
    if opcao_sexo:
        if opcao_sexo in OPCOES_SEXO:
            cliente["sexo"] = OPCOES_SEXO[opcao_sexo]
        else:
            print("\n[ERRO] Opção de sexo inválida. Alteração abortada.")
            return

    novo_telefone = input(f"Telefone atual [{cliente['telefone']}]: ").strip()
    novo_endereco = input(f"Endereço atual [{cliente['endereco']}]: ").strip()

    if novo_nome:
        cliente["nome"] = novo_nome
    if novo_telefone:
        cliente["telefone"] = novo_telefone
    if novo_endereco:
        cliente["endereco"] = novo_endereco

    salvar_dados(dados)
    print("\n[SUCESSO] Dados do cliente atualizados com sucesso!")


def cancelar_cliente(dados):
    print("\n" + "=" * 45)
    print("        CANCELAR CADASTRO DE CLIENTE")
    print("=" * 45)

    cliente = selecionar_cliente_interativo(dados)
    if cliente is None:
        return

    if cliente["status"] == "Cancelado":
        print("\n[AVISO] Este cliente já está com o cadastro cancelado.")
        return

    veiculos_ativos = [
        v for v in dados["veiculos"]
        if v["cpf_cliente"] == cliente["cpf"] and v["status"] == "Ativo"
    ]

    if veiculos_ativos:
        placas = ", ".join(v["placa"] for v in veiculos_ativos)
        print(f"\n[ERRO] Não é possível cancelar o cliente '{cliente['nome']}'.")
        print(f"Motivo: Possui veículo(s) ativo(s) vinculado(s): {placas}.")
        print("Cancele os veículos primeiro antes de cancelar o cliente.")
        return

    print(f"\nCliente selecionado: {cliente['nome']} (CPF: {cliente['cpf']})")
    if confirmar_acao("Tem certeza que deseja cancelar este cadastro?"):
        cliente["status"] = "Cancelado"
        salvar_dados(dados)
        print("\n[SUCESSO] Cadastro do cliente cancelado (histórico preservado).")
    else:
        print("\n[INFO] Operação de cancelamento abortada.")


def reativar_cliente(dados):
    print("\n" + "=" * 45)
    print("        REATIVAR CADASTRO DE CLIENTE")
    print("=" * 45)

    cliente = selecionar_cliente_interativo(dados)
    if cliente is None:
        return

    if cliente["status"] == "Ativo":
        print("\n[AVISO] Este cliente já está com o cadastro ativo.")
        return

    print(f"\nCliente selecionado: {cliente['nome']} (CPF: {cliente['cpf']})")
    if confirmar_acao("Deseja reativar este cadastro?"):
        cliente["status"] = "Ativo"
        salvar_dados(dados)
        print("\n[SUCESSO] Cadastro do cliente reativado com sucesso!")
    else:
        print("\n[INFO] Operação de reativação abortada.")
