
import Pyro5.api


class GerenciadorFalhas:

    def __init__(self):
        self.controladores = [
            ("Controlador 1", "PYRO:controlador1@localhost:50001"),
            ("Controlador 2", "PYRO:controlador2@localhost:50002")
        ]

    def obter_controlador_disponivel(self):

        for nome, uri in self.controladores:
            try:
                controlador = Pyro5.api.Proxy(uri)

                resultado = controlador.verificar_disponibilidade()

                if resultado["disponivel"]:
                    print(nome + " selecionado.")
                    return controlador

            except Exception:
                print(nome + " indisponível.")

        return None
