
import Pyro5.api


# Endereço remoto do controlador 2
URI = "PYRO:controlador2@localhost:50002"


try:
    controlador = Pyro5.api.Proxy(URI)

    print(controlador.obter_status())

    obras = controlador.listar_obras()

    print("\nObras cadastradas:")

    if obras:
        for obra in obras:
            print(obra)
    else:
        print("Nenhuma obra cadastrada.")

except Exception as erro:
    print("Erro ao comunicar com o controlador:", erro)
