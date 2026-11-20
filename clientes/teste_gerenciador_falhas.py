
import sys
from pathlib import Path

import Pyro5.api

# Adiciona a pasta principal do projeto ao caminho de importação
PASTA_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PASTA_PROJETO))

from controladores.gerenciador_falhas import GerenciadorFalhas


gerenciador = GerenciadorFalhas()

controlador = gerenciador.obter_controlador_disponivel()

if controlador is not None:
    try:
        resultado = controlador.verificar_disponibilidade()

        print("\nConexão estabelecida com sucesso!")
        print("Controlador selecionado:", resultado["controlador"])

    finally:
        controlador._pyroRelease()

else:
    print("\nNenhum controlador está disponível.")
