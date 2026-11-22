
import Pyro5.api


class GerenciadorFalhas:

    def __init__(self):
        self.controladores = [
            ("Controlador 1", "PYRO:controlador1@localhost:50001"),
            ("Controlador 2", "PYRO:controlador2@localhost:50002")
        ]

    def obter_controlador_disponivel(self):

        self.verificar_recuperacao()

        # Primeiro, verifica o Controlador 1    
        try:
            controlador = Pyro5.api.Proxy(
                "PYRO:controlador1@localhost:50001"
            )

            resultado = controlador.verificar_disponibilidade()

            if resultado["disponivel"]:
                papel = controlador.obter_papel()

                if papel == "Principal":
                    print("Controlador 1 selecionado.")
                    return controlador

        except Exception:
            print("Controlador 1 indisponível.")

        # Se o Controlador 1 falhar, tenta o Controlador 2
        try:
            controlador = Pyro5.api.Proxy(
                "PYRO:controlador2@localhost:50002"
            )

            resultado = controlador.verificar_disponibilidade()

            if resultado["disponivel"]:
                papel = controlador.obter_papel()

                if papel != "Principal":
                    controlador.assumir_principal()

                print("Controlador 2 assumiu como Principal.")
                return controlador

        except Exception:
            print("Controlador 2 indisponível.")

        return None

    def promover_controlador_reserva(self):
        uri = "PYRO:controlador2@localhost:50002"

        try:
            controlador = Pyro5.api.Proxy(uri)

            resultado = controlador.assumir_principal()

            print(resultado)

            controlador._pyroRelease()

            return True

        except Exception as erro:
            print("Erro ao promover Controlador 2:", erro)
            return False

    def promover_controlador1(self):
        uri = "PYRO:controlador1@localhost:50001"

        try:
            controlador = Pyro5.api.Proxy(uri)

            resultado = controlador.assumir_principal()

            print(resultado)

            controlador._pyroRelease()

            return True

        except Exception as erro:
            print("Erro ao promover Controlador 1:", erro)
            return False

    def verificar_recuperacao(self):
        try:
            controlador1 = Pyro5.api.Proxy(
                "PYRO:controlador1@localhost:50001"
            )

            controlador2 = Pyro5.api.Proxy(
                "PYRO:controlador2@localhost:50002"
            )

            disponibilidade1 = controlador1.verificar_disponibilidade()
            disponibilidade2 = controlador2.verificar_disponibilidade()

            if disponibilidade1["disponivel"] and disponibilidade2["disponivel"]:

                papel2 = controlador2.obter_papel()

                if papel2 == "Principal":
                    controlador1.assumir_reserva()
                    print("Controlador 1 permanece como Reserva.")
                    print("Controlador 2 continua como Principal.")

                    return True

            return False

        except Exception as erro:
            print("Erro ao verificar recuperação:", erro)
            return False
