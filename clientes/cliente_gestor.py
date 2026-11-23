
import sys
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PASTA_PROJETO))

from controladores.gerenciador_falhas import GerenciadorFalhas


def consultar_obras():
    gerenciador = GerenciadorFalhas()

    controlador = gerenciador.obter_controlador_disponivel()

    if controlador is None:
        print("\nNão foi possível consultar as obras.")
        return

    try:
        obras = controlador.listar_obras()

        print("\n========== OBRAS CADASTRADAS ==========")

        if not obras:
            print("Nenhuma obra cadastrada.")
            return

        for obra in obras:
            print(f"\nID: {obra['id_obra']}")
            print(f"Nome: {obra['nome']}")
            print(f"Localização: {obra['localizacao']}")
            print(f"Status: {obra['status']}")

    except Exception as erro:
        print("\nErro ao consultar obras:", erro)

    finally:
        controlador._pyroRelease()


def cadastrar_obra():
    print("\n========== CADASTRAR OBRA ==========")

    nome = input("Nome da obra: ")
    localizacao = input("Localização: ")
    descricao = input("Descrição: ")
    data_inicio = input("Data de início (AAAA-MM-DD): ")
    status = input("Status: ")

    gerenciador = GerenciadorFalhas()
    controlador = gerenciador.obter_controlador_disponivel()

    if controlador is None:
        print("\nNão foi possível cadastrar a obra.")
        return

    try:
        resultado = controlador.cadastrar_obra(
            nome,
            localizacao,
            descricao,
            data_inicio,
            status
        )

        print("\nResultado do cadastro:")
        print(resultado["mensagem"])

        if resultado["sucesso"]:
            print("ID da obra:", resultado["id_obra"])

        if "erro" in resultado:
            print("Detalhes:", resultado["erro"])

    except Exception as erro:
        print("\nErro ao cadastrar obra:", erro)

    finally:
        controlador._pyroRelease()



def menu():
    while True:
        print("\n========== CLIENTE GESTOR ==========")
        print("1 - Consultar obras")
        print("2 - Cadastrar obra")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            consultar_obras()

        elif opcao == "2":
            cadastrar_obra()

        elif opcao == "0":
            print("\nEncerrando o cliente gestor...")
            break

        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    menu()
