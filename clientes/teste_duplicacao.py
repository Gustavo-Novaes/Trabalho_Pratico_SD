
import Pyro5.api

URI = "PYRO:controlador2@localhost:50002"

try:
    controlador = Pyro5.api.Proxy(URI)

    resultado = controlador.registrar_obra_replica(
        1,
        "Obra Geotécnica 01",
        "Congonhas - MG",
        "Obra utilizada para testar a replicação",
        "2026-11-19",
        "Em andamento"
    )

    print("\nResultado do teste:")
    print(resultado)

except Exception as erro:
    print("Erro ao comunicar com o Controlador 2:", erro)
