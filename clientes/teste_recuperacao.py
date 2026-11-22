import sys
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PASTA_PROJETO))

from controladores.gerenciador_falhas import GerenciadorFalhas

gerenciador = GerenciadorFalhas()

resultado = gerenciador.verificar_recuperacao()

if resultado:
    print("\nRecuperação verificada com sucesso!")
else:
    print("\nNão foi possível verificar a recuperação.")