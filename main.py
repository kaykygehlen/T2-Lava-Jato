from dados import carregar_dados, pausar
from clientes import (
    cadastrar_cliente,
    listar_clientes,
    consultar_cliente,
    alterar_cliente,
    cancelar_cliente,
    reativar_cliente
)
from veiculos import (
    cadastrar_veiculo,
    listar_veiculos,
    consultar_veiculo,
    alterar_veiculo,
    cancelar_veiculo,
    reativar_veiculo
)
from servicos import (
    registrar_lavagem,
    concluir_servico_aberto,
    historico_lavagens,
    cancelar_servico,
    consultar_servicos_por_placa,
    relatorio_financeiro
)


def exibir_menu():
    print("\n" + "=" * 45)
    print("     SISTEMA DE GERENCIAMENTO DE LAVA-JATO")
    print("=" * 45)
    print("1  - Cadastrar cliente")
    print("2  - Listar clientes")
    print("3  - Consultar cliente (CPF ou Nome)")
    print("4  - Alterar cliente")
    print("5  - Cancelar cadastro de cliente")
    print("6  - Reativar cadastro de cliente")
    print("-" * 45)
    print("7  - Cadastrar veículo")
    print("8  - Listar veículos")
    print("9  - Consultar veículo")
    print("10 - Alterar veículo")
    print("11 - Cancelar cadastro de veículo")
    print("12 - Reativar cadastro de veículo")
    print("-" * 45)
    print("13 - Registrar lavagem (Concluída ou Em Aberto)")
    print("14 - Finalizar / Receber serviço em aberto")
    print("15 - Histórico de lavagens")
    print("16 - Cancelar serviço")
    print("17 - Consultar serviços por placa")
    print("18 - Relatório financeiro")
    print("-" * 45)
    print("0  - Sair do sistema")
    print("=" * 45)


def main():
    dados = carregar_dados()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_cliente(dados)
            pausar()
        elif opcao == "2":
            listar_clientes(dados)
            pausar()
        elif opcao == "3":
            consultar_cliente(dados)
            pausar()
        elif opcao == "4":
            alterar_cliente(dados)
            pausar()
        elif opcao == "5":
            cancelar_cliente(dados)
            pausar()
        elif opcao == "6":
            reativar_cliente(dados)
            pausar()
        elif opcao == "7":
            cadastrar_veiculo(dados)
            pausar()
        elif opcao == "8":
            listar_veiculos(dados)
            pausar()
        elif opcao == "9":
            consultar_veiculo(dados)
            pausar()
        elif opcao == "10":
            alterar_veiculo(dados)
            pausar()
        elif opcao == "11":
            cancelar_veiculo(dados)
            pausar()
        elif opcao == "12":
            reativar_veiculo(dados)
            pausar()
        elif opcao == "13":
            registrar_lavagem(dados)
            pausar()
        elif opcao == "14":
            concluir_servico_aberto(dados)
            pausar()
        elif opcao == "15":
            historico_lavagens(dados)
            pausar()
        elif opcao == "16":
            cancelar_servico(dados)
            pausar()
        elif opcao == "17":
            consultar_servicos_por_placa(dados)
            pausar()
        elif opcao == "18":
            relatorio_financeiro(dados)
            pausar()
        elif opcao == "0":
            print("\nEncerrando o sistema... Todos os dados estão salvos. Até logo!")
            break
        else:
            print("\n[ERRO] Opção inválida! Escolha um número entre 0 e 18.")
            pausar()


if __name__ == "__main__":
    main()
