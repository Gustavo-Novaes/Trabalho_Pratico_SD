
import Pyro5.api


URI = "PYRO:controlador1@localhost:50001"

try:
    controlador = Pyro5.api.Proxy(URI)

    resultado = controlador.cadastrar_obra(
        "Obra Geotécnica 01",
        "Congonhas - MG",
        "Obra utilizada para testar a replicação",
        "2026-11-19",
        "Em andamento"
    )

    print("\nResultado do cadastro:")
    print(resultado["mensagem"])
    print("ID da obra:", resultado["id_obra"])

    if "erro" in resultado:
        print("Detalhes:", resultado["erro"])

except Exception as erro:
    print("Erro ao comunicar com o controlador:", erro)
