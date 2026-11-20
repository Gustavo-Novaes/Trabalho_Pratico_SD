
import Pyro5.api

CONTROLADORES = {
    "Controlador 1": "PYRO:controlador1@localhost:50001",
    "Controlador 2": "PYRO:controlador2@localhost:50002"
}

for nome, uri in CONTROLADORES.items():
    try:
        controlador = Pyro5.api.Proxy(uri)

        resultado = controlador.verificar_disponibilidade()

        if resultado["disponivel"]:
            print(nome + ": Disponível")
        else:
            print(nome + ": Indisponível")

    except Exception:
        print(nome + ": Indisponível")
