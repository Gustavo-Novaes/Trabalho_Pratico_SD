
import sys
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PASTA_PROJETO))

from controladores.gerenciador_falhas import GerenciadorFalhas


gerenciador = GerenciadorFalhas()

controlador = gerenciador.obter_controlador_disponivel()

if controlador is not None:
    try:
        obras = controlador.listar_obras()

        print("\nObras cadastradas:")

        if obras:
            for obra in obras:
                print(
                    f"ID: {obra['id_obra']} | "
                    f"Nome: {obra['nome']} | "
                    f"Localização: {obra['localizacao']}"
                )
        else:
            print("Nenhuma obra cadastrada.")

    except Exception as erro:
        print("Erro ao consultar as obras:", erro)

    finally:
        controlador._pyroRelease()

else:
    print("\nNenhum controlador está disponível.")
