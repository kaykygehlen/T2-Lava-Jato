from datetime import datetime
from dados import salvar_dados, formatar_placa, confirmar_acao
from veiculos import buscar_veiculo_por_placa
from clientes import buscar_cliente_por_cpf


TIPOS_LAVAGEM = {
    "1": "Lavagem Simples (Externa)",
    "2": "Lavagem Completa (Externa + Interna)",
    "3": "Lavagem com Cera / Polimento",
    "4": "Higienização Interna Completa",
    "5": "Lavagem de Motor"
}

FORMAS_PAGAMENTO = {
    "1": "Dinheiro",
    "2": "Pix",
    "3": "Cartão de débito",
    "4": "Cartão de crédito"
}


def registrar_lavagem(dados):
    print("\n" + "=" * 45)
    print("            REGISTRAR LAVAGEM")
    print("=" * 45)

    placa = input("Informe a placa do veículo: ").strip()
    veiculo = buscar_veiculo_por_placa(dados, placa)

    if veiculo is None:
        print("\n[ERRO] Veículo não encontrado. Cadastre o veículo primeiro.")
        return

    if veiculo["status"] != "Ativo":
        print("\n[ERRO] Não é possível registrar serviço para um veículo com cadastro cancelado.")
        return

    proprietario = buscar_cliente_por_cpf(dados, veiculo["cpf_cliente"])
    nome_prop = proprietario["nome"] if proprietario else "Desconhecido"

    print(f"\nVeículo:      {veiculo['marca']} {veiculo['modelo']} ({veiculo['cor']})")
    print(f"Proprietário: {nome_prop} (CPF: {veiculo['cpf_cliente']})")

    print("\nTipos de Lavagem:")
    for codigo, descricao in TIPOS_LAVAGEM.items():
        print(f"  {codigo} - {descricao}")

    opcao_lavagem = input("Escolha o tipo de lavagem: ").strip()
    if opcao_lavagem not in TIPOS_LAVAGEM:
        print("\n[ERRO] Opção de lavagem inválida.")
        return
    tipo_lavagem = TIPOS_LAVAGEM[opcao_lavagem]

    try:
        valor_str = input("Valor do serviço (R$): ").strip().replace(",", ".")
        valor = float(valor_str)
        if valor <= 0:
            print("\n[ERRO] O valor do serviço deve ser maior que zero.")
            return
    except ValueError:
        print("\n[ERRO] Valor inválido! Digite um número (ex: 50.00).")
        return

    print("\nSituação do Atendimento:")
    print("  1 - Concluído / Pago agora")
    print("  2 - Em Aberto (Pagar na retirada / Em execução)")
    situacao = input("Escolha a situação: ").strip()

    if situacao == "1":
        print("\nFormas de Pagamento:")
        for codigo, forma in FORMAS_PAGAMENTO.items():
            print(f"  {codigo} - {forma}")

        opcao_pagamento = input("Escolha a forma de pagamento: ").strip()
        if opcao_pagamento not in FORMAS_PAGAMENTO:
            print("\n[ERRO] Forma de pagamento inválida.")
            return
        forma_pagamento = FORMAS_PAGAMENTO[opcao_pagamento]
        status_servico = "Concluído"
    elif situacao == "2":
        forma_pagamento = "A definir"
        status_servico = "Em Aberto"
    else:
        print("\n[ERRO] Opção de situação inválida.")
        return

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    data_custom = input(f"Data e hora [{agora}] (ENTER para usar atual): ").strip()
    data_hora = data_custom if data_custom else agora

    novo_id = 1 if not dados["servicos"] else dados["servicos"][-1]["id"] + 1

    novo_servico = {
        "id": novo_id,
        "placa": veiculo["placa"],
        "cpf_cliente": veiculo["cpf_cliente"],
        "nome_cliente": nome_prop,
        "tipo_lavagem": tipo_lavagem,
        "valor": valor,
        "forma_pagamento": forma_pagamento,
        "data_hora": data_hora,
        "status": status_servico
    }

    dados["servicos"].append(novo_servico)
    salvar_dados(dados)
    print(f"\n[SUCESSO] Lavagem #{novo_id} registrada com status [{status_servico}]! Valor: R$ {valor:.2f}")


def concluir_servico_aberto(dados):
    print("\n" + "=" * 65)
    print("              CONCLUIR / RECEBER SERVIÇO EM ABERTO")
    print("=" * 65)

    servicos_abertos = [s for s in dados["servicos"] if s["status"] == "Em Aberto"]

    if not servicos_abertos:
        print("Não há nenhum serviço em aberto no momento.")
        return

    print("Serviços atualmente EM ABERTO:")
    print("-" * 65)
    for s in servicos_abertos:
        print(f"ID #{s['id']} | Placa: {s['placa']} | Cliente: {s['nome_cliente']}")
        print(f"Serviço: {s['tipo_lavagem']} | Valor: R$ {s['valor']:.2f} | Entrada: {s['data_hora']}")
        print("-" * 65)

    try:
        id_busca = int(input("Informe o ID do serviço que deseja finalizar e receber: ").strip())
    except ValueError:
        print("\n[ERRO] ID inválido! Digite um número inteiro.")
        return

    servico_encontrado = None
    for s in servicos_abertos:
        if s["id"] == id_busca:
            servico_encontrado = s
            break

    if servico_encontrado is None:
        print("\n[ERRO] ID não encontrado entre os serviços em aberto.")
        return

    print("\nFormas de Pagamento:")
    for codigo, forma in FORMAS_PAGAMENTO.items():
        print(f"  {codigo} - {forma}")

    opcao_pagamento = input("Escolha a forma de pagamento recebida: ").strip()
    if opcao_pagamento not in FORMAS_PAGAMENTO:
        print("\n[ERRO] Forma de pagamento inválida.")
        return

    servico_encontrado["forma_pagamento"] = FORMAS_PAGAMENTO[opcao_pagamento]
    servico_encontrado["status"] = "Concluído"
    salvar_dados(dados)
    print(f"\n[SUCESSO] Serviço #{servico_encontrado['id']} finalizado e pago via {servico_encontrado['forma_pagamento']}!")


def historico_lavagens(dados):
    print("\n" + "=" * 70)
    print("                    HISTÓRICO GERAL DE LAVAGENS")
    print("=" * 70)

    if not dados["servicos"]:
        print("Nenhum serviço registrado no sistema.")
        return

    for s in dados["servicos"]:
        print(f"ID #{s['id']} | Data: {s['data_hora']} | Status: [{s['status']}]")
        print(f"Placa: {s['placa']} | Cliente: {s['nome_cliente']}")
        print(f"Serviço: {s['tipo_lavagem']} | Valor: R$ {s['valor']:.2f} ({s['forma_pagamento']})")
        print("-" * 70)


def cancelar_servico(dados):
    print("\n" + "=" * 45)
    print("             CANCELAR SERVIÇO")
    print("=" * 45)

    try:
        id_busca = int(input("Informe o ID do serviço que deseja cancelar: ").strip())
    except ValueError:
        print("\n[ERRO] ID inválido! Digite um número inteiro.")
        return

    servico_encontrado = None
    for s in dados["servicos"]:
        if s["id"] == id_busca:
            servico_encontrado = s
            break

    if servico_encontrado is None:
        print("\n[ERRO] Serviço não encontrado com o ID informado.")
        return

    if servico_encontrado["status"] == "Cancelado":
        print("\n[AVISO] Este serviço já está cancelado.")
        return

    print(f"\nServiço #{servico_encontrado['id']} - Placa: {servico_encontrado['placa']} [{servico_encontrado['status']}]")
    print(f"Descrição: {servico_encontrado['tipo_lavagem']} | Valor: R$ {servico_encontrado['valor']:.2f}")

    if confirmar_acao("Tem certeza que deseja cancelar este serviço?"):
        servico_encontrado["status"] = "Cancelado"
        salvar_dados(dados)
        print("\n[SUCESSO] Serviço cancelado (registro preservado no histórico).")
    else:
        print("\n[INFO] Operação de cancelamento abortada.")


def consultar_servicos_por_placa(dados):
    print("\n" + "=" * 65)
    print("               HISTÓRICO DE SERVIÇOS POR PLACA")
    print("=" * 65)

    placa = formatar_placa(input("Informe a placa do veículo: "))
    if not placa:
        print("\n[ERRO] Placa não informada.")
        return

    servicos_veiculo = [s for s in dados["servicos"] if s["placa"] == placa]

    if not servicos_veiculo:
        print(f"\n[AVISO] Nenhum serviço registrado para a placa {placa}.")
        return

    print(f"\nHistórico da placa {placa} ({len(servicos_veiculo)} registro(s)):")
    print("-" * 65)
    for s in servicos_veiculo:
        print(f"ID #{s['id']} | {s['data_hora']} | {s['tipo_lavagem']}")
        print(f"Valor: R$ {s['valor']:.2f} | Pagamento: {s['forma_pagamento']} | Status: [{s['status']}]")
        print("-" * 65)


def relatorio_financeiro(dados):
    print("\n" + "=" * 55)
    print("                 RELATÓRIO FINANCEIRO")
    print("=" * 55)

    totais_pagamento = {
        "Dinheiro": 0.0,
        "Pix": 0.0,
        "Cartão de débito": 0.0,
        "Cartão de crédito": 0.0
    }

    total_recebido = 0.0
    qtd_concluidos = 0
    total_aberto = 0.0
    qtd_abertos = 0
    total_cancelado = 0.0
    qtd_cancelados = 0

    for s in dados["servicos"]:
        if s["status"] == "Concluído":
            total_recebido += s["valor"]
            qtd_concluidos += 1
            forma = s["forma_pagamento"]
            if forma in totais_pagamento:
                totais_pagamento[forma] += s["valor"]
        elif s["status"] == "Em Aberto":
            total_aberto += s["valor"]
            qtd_abertos += 1
        elif s["status"] == "Cancelado":
            total_cancelado += s["valor"]
            qtd_cancelados += 1

    print(f"Serviços Concluídos (Pagos): {qtd_concluidos}")
    print(f"Serviços Em Aberto:          {qtd_abertos} (A receber: R$ {total_aberto:.2f})")
    print(f"Serviços Cancelados:         {qtd_cancelados} (Cancelado: R$ {total_cancelado:.2f})")
    print("-" * 55)
    print("Entradas Recebidas por Forma de Pagamento:")
    for forma, valor in totais_pagamento.items():
        print(f"  - {forma:<20}: R$ {valor:>10.2f}")
    print("-" * 55)
    print(f"TOTAL GERAL EM CAIXA:     R$ {total_recebido:>10.2f}")
    print("=" * 55)
