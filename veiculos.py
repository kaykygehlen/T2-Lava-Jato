from dados import salvar_dados, formatar_placa, confirmar_acao
from clientes import buscar_cliente_por_cpf, selecionar_cliente_interativo


def buscar_veiculo_por_placa(dados, placa):
    """Retorna o dicionário do veículo pela placa ou None se não encontrar."""
    placa_formatada = formatar_placa(placa)
    for veiculo in dados["veiculos"]:
        if veiculo["placa"] == placa_formatada:
            return veiculo
    return None


def cadastrar_veiculo(dados):
    print("\n" + "=" * 45)
    print("           CADASTRAR NOVO VEÍCULO")
    print("=" * 45)

    print("Localize o proprietário do veículo:")
    cliente = selecionar_cliente_interativo(dados)

    if cliente is None:
        return

    if cliente["status"] != "Ativo":
        print("\n[ERRO] O cliente informado está com o cadastro cancelado.")
        return

    print(f"Proprietário selecionado: {cliente['nome']} (CPF: {cliente['cpf']})")
    placa_input = input("Placa do veículo (ex: ABC1D23 ou ABC-1234): ").strip()
    placa = formatar_placa(placa_input)

    if len(placa) != 7:
        print("\n[ERRO] Placa inválida! A placa deve conter 7 caracteres.")
        return

    if buscar_veiculo_por_placa(dados, placa) is not None:
        print("\n[ERRO] Já existe um veículo cadastrado com esta placa.")
        return

    marca = input("Marca (ex: Toyota, Fiat, VW): ").strip()
    modelo = input("Modelo (ex: Corolla, Argo, Gol): ").strip()
    cor = input("Cor: ").strip()

    if not marca or not modelo or not cor:
        print("\n[ERRO] Marca, modelo e cor são campos obrigatórios.")
        return

    try:
        ano = int(input("Ano de fabricação (ex: 2022): ").strip())
        if ano < 1900 or ano > 2027:
            print("\n[ERRO] Ano inválido.")
            return
    except ValueError:
        print("\n[ERRO] O ano deve ser um número inteiro válido.")
        return

    novo_veiculo = {
        "placa": placa,
        "marca": marca,
        "modelo": modelo,
        "cor": cor,
        "ano": ano,
        "cpf_cliente": cliente["cpf"],
        "status": "Ativo"
    }

    dados["veiculos"].append(novo_veiculo)
    salvar_dados(dados)
    print(f"\n[SUCESSO] Veículo {marca} {modelo} ({placa}) vinculado a {cliente['nome']}!")


def listar_veiculos(dados):
    print("\n" + "=" * 65)
    print("                      LISTA DE VEÍCULOS")
    print("=" * 65)

    if not dados["veiculos"]:
        print("Nenhum veículo cadastrado no sistema.")
        return

    for v in dados["veiculos"]:
        proprietario = buscar_cliente_por_cpf(dados, v["cpf_cliente"])
        nome_prop = proprietario["nome"] if proprietario else "Desconhecido"
        print(f"Placa: {v['placa']} | {v['marca']} {v['modelo']} ({v['ano']}) - Cor: {v['cor']} | [{v['status']}]")
        print(f"Proprietário: {nome_prop} (CPF: {v['cpf_cliente']})")
        print("-" * 65)


def consultar_veiculo(dados):
    print("\n" + "=" * 45)
    print("             CONSULTAR VEÍCULO")
    print("=" * 45)

    placa = input("Digite a placa do veículo: ").strip()
    veiculo = buscar_veiculo_por_placa(dados, placa)

    if veiculo is None:
        print("\n[AVISO] Nenhum veículo encontrado com esta placa.")
        return

    proprietario = buscar_cliente_por_cpf(dados, veiculo["cpf_cliente"])
    nome_prop = proprietario["nome"] if proprietario else "Não encontrado"

    print("\n" + "-" * 50)
    print(f"Placa:        {veiculo['placa']} ({veiculo['status']})")
    print(f"Veículo:      {veiculo['marca']} {veiculo['modelo']}")
    print(f"Cor / Ano:    {veiculo['cor']} / {veiculo['ano']}")
    print(f"Proprietário: {nome_prop} (CPF: {veiculo['cpf_cliente']})")
    print("-" * 50)


def alterar_veiculo(dados):
    print("\n" + "=" * 45)
    print("         ALTERAR DADOS DO VEÍCULO")
    print("=" * 45)

    placa = input("Informe a placa do veículo que deseja alterar: ").strip()
    veiculo = buscar_veiculo_por_placa(dados, placa)

    if veiculo is None:
        print("\n[ERRO] Veículo não encontrado.")
        return

    if veiculo["status"] == "Cancelado":
        print("\n[ERRO] Não é possível alterar um veículo cancelado.")
        return

    print(f"\nEditando veículo: {veiculo['marca']} {veiculo['modelo']} ({veiculo['placa']})")
    print("(Deixe em branco e pressione ENTER para manter o valor atual)\n")

    nova_marca = input(f"Marca atual [{veiculo['marca']}]: ").strip()
    novo_modelo = input(f"Modelo atual [{veiculo['modelo']}]: ").strip()
    nova_cor = input(f"Cor atual [{veiculo['cor']}]: ").strip()
    novo_ano_str = input(f"Ano atual [{veiculo['ano']}]: ").strip()

    if novo_ano_str:
        try:
            novo_ano = int(novo_ano_str)
            if 1900 <= novo_ano <= 2027:
                veiculo["ano"] = novo_ano
            else:
                print("\n[ERRO] Ano fora do intervalo permitido. Alteração abortada.")
                return
        except ValueError:
            print("\n[ERRO] Ano inválido. Digite apenas números. Alteração abortada.")
            return

    if nova_marca:
        veiculo["marca"] = nova_marca
    if novo_modelo:
        veiculo["modelo"] = novo_modelo
    if nova_cor:
        veiculo["cor"] = nova_cor

    salvar_dados(dados)
    print("\n[SUCESSO] Dados do veículo atualizados com sucesso!")


def cancelar_veiculo(dados):
    print("\n" + "=" * 45)
    print("        CANCELAR CADASTRO DE VEÍCULO")
    print("=" * 45)

    placa = input("Informe a placa do veículo: ").strip()
    veiculo = buscar_veiculo_por_placa(dados, placa)

    if veiculo is None:
        print("\n[ERRO] Veículo não encontrado.")
        return

    if veiculo["status"] == "Cancelado":
        print("\n[AVISO] Este veículo já está com o cadastro cancelado.")
        return

    print(f"\nVeículo selecionado: {veiculo['marca']} {veiculo['modelo']} - Placa: {veiculo['placa']}")
    if confirmar_acao("Tem certeza que deseja cancelar este veículo?"):
        veiculo["status"] = "Cancelado"
        salvar_dados(dados)
        print("\n[SUCESSO] Cadastro do veículo cancelado (histórico preservado).")
    else:
        print("\n[INFO] Operação de cancelamento abortada.")


def reativar_veiculo(dados):
    print("\n" + "=" * 45)
    print("        REATIVAR CADASTRO DE VEÍCULO")
    print("=" * 45)

    placa = input("Informe a placa do veículo que deseja reativar: ").strip()
    veiculo = buscar_veiculo_por_placa(dados, placa)

    if veiculo is None:
        print("\n[ERRO] Veículo não encontrado.")
        return

    if veiculo["status"] == "Ativo":
        print("\n[AVISO] Este veículo já está com o cadastro ativo.")
        return

    proprietario = buscar_cliente_por_cpf(dados, veiculo["cpf_cliente"])
    if proprietario is None or proprietario["status"] != "Ativo":
        print("\n[ERRO] Não é possível reativar este veículo.")
        print("Motivo: O proprietário vinculado está com o cadastro cancelado. Reative o cliente primeiro.")
        return

    print(f"\nVeículo selecionado: {veiculo['marca']} {veiculo['modelo']} - Placa: {veiculo['placa']}")
    print(f"Proprietário: {proprietario['nome']}")
    if confirmar_acao("Deseja reativar este veículo?"):
        veiculo["status"] = "Ativo"
        salvar_dados(dados)
        print("\n[SUCESSO] Cadastro do veículo reativado com sucesso!")
    else:
        print("\n[INFO] Operação de reativação abortada.")
