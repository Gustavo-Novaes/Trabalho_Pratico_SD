import Pyro5.api

CONTROLADORES = {
    "Controlador 1": "PYRO:controlador1@localhost:50001",
    "Controlador 2": "PYRO:controlador2@localhost:50002"
}

for nome, uri in CONTROLADORES.items():
    try:
        controlador = Pyro5.api.Proxy(uri)
        papel = controlador.obter_papel()

        print(f"{nome} - Papel: {papel}")

        controlador._pyroRelease()

    except Exception as erro:
        print(f"{nome} - Erro: {erro}")