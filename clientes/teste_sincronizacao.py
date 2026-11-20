
import Pyro5.api

URI = "PYRO:controlador1@localhost:50001"

try:
    controlador = Pyro5.api.Proxy(URI)

    resultado = controlador.sincronizar_pendencias()

    print("\nResultado da sincronização:")
    print("Total de pendências:", resultado["total_pendentes"])
    print("Obras sincronizadas:", resultado["sincronizadas"])

    if resultado["erros"]:
        print("\nOcorreram erros:")

        for erro in resultado["erros"]:
            print("Obra ID:", erro["id_obra"])
            print("Erro:", erro["erro"])

    else:
        print("\nTodas as pendências foram processadas!")

except Exception as erro:
    print("Erro ao comunicar com o controlador:", erro)
