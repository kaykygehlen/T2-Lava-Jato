import json
import os

ARQUIVO_DADOS = "dados.json"


def carregar_dados():
    """Lê os dados do arquivo JSON. Se não existir ou estiver corrompido, cria a estrutura padrão."""
    estrutura_padrao = {
        "clientes": [],
        "veiculos": [],
        "servicos": []
    }
    if not os.path.exists(ARQUIVO_DADOS):
        salvar_dados(estrutura_padrao)
        return estrutura_padrao

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            for chave in estrutura_padrao:
                if chave not in dados:
                    dados[chave] = []
            return dados
    except (json.JSONDecodeError, IOError):
        print("\n[AVISO] Arquivo de dados corrompido ou ilegível. Criando nova base.")
        salvar_dados(estrutura_padrao)
        return estrutura_padrao


def salvar_dados(dados):
    """Grava o dicionário completo de dados no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    except IOError as erro:
        print(f"\n[ERRO] Não foi possível salvar os dados: {erro}")


def limpar_texto_numerico(texto):
    """Remove pontos, traços e espaços de strings como CPF ou telefone."""
    return "".join(char for char in texto if char.isdigit())


def formatar_placa(placa):
    """Padroniza a placa em letras maiúsculas e sem espaços ou hífens."""
    return placa.strip().upper().replace("-", "").replace(" ", "")


def confirmar_acao(mensagem):
    """Solicita confirmação (S/N) antes de operações críticas."""
    while True:
        resposta = input(f"{mensagem} (S/N): ").strip().upper()
        if resposta == "S":
            return True
        elif resposta == "N":
            return False
        else:
            print("[ERRO] Entrada inválida. Digite 'S' para Sim ou 'N' para Não.")


def pausar():
    """Pausa a execução para o usuário ler as mensagens antes de voltar ao menu."""
    input("\nPressione ENTER para continuar...")
