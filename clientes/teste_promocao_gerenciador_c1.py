import sys
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PASTA_PROJETO))

from controladores.gerenciador_falhas import GerenciadorFalhas

gerenciador = GerenciadorFalhas()

resultado = gerenciador.promover_controlador1()

if resultado:
    print("\nPromoção realizada com sucesso!")
else:
    print("\nNão foi possível realizar a promoção.")