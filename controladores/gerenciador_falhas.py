import Pyro5.api


class GerenciadorFalhas:

    def __init__(self):
        self.controladores = [
            ("Controlador 1", "PYRO:controlador1@localhost:50001"),
            ("Controlador 2", "PYRO:controlador2@localhost:50002")
        ]

    
    def obter_controlador_disponivel(self):
        # Verifica o Controlador 1
        controlador1 = None
        try:
            controlador1 = Pyro5.api.Proxy(
                "PYRO:controlador1@localhost:50001"
            )
            disponibilidade1 = controlador1.verificar_disponibilidade()
            if not disponibilidade1["disponivel"]:
                controlador1 = None
        except Exception:
            print("Controlador 1 indisponível.")
            controlador1 = None

        # Verifica o Controlador 2
        controlador2 = None
        try:
            controlador2 = Pyro5.api.Proxy(
                "PYRO:controlador2@localhost:50002"
            )
            disponibilidade2 = controlador2.verificar_disponibilidade()
            if not disponibilidade2["disponivel"]:
                controlador2 = None
        except Exception:
            print("Controlador 2 indisponível.")
            controlador2 = None

        # Caso ambos estejam indisponíveis
        if controlador1 is None and controlador2 is None:
            print("\nNenhum controlador está disponível.")
            return None

        # Caso somente o Controlador 1 esteja disponível
        if controlador1 is not None and controlador2 is None:
            if controlador1.obter_papel() != "Principal":
                print("Promovendo Controlador 1...")
                resultado = controlador1.assumir_principal()
                print(resultado)

            print("Controlador 1 selecionado.")
            return controlador1

        # Caso somente o Controlador 2 esteja disponível
        if controlador1 is None and controlador2 is not None:
            if controlador2.obter_papel() != "Principal":
                print("Promovendo Controlador 2...")
                controlador2.assumir_principal()

            print("Controlador 2 selecionado.")
            return controlador2

        # Caso ambos estejam disponíveis
        papel1 = controlador1.obter_papel()
        papel2 = controlador2.obter_papel()

        if papel2 == "Principal":
            if papel1 != "Reserva":
                controlador1.assumir_reserva()

            print("Controlador 2 selecionado.")
            return controlador2

        if papel1 == "Principal":
            print("Controlador 1 selecionado.")
            return controlador1

        # Se nenhum for Principal, promove o Controlador 1
        print("Nenhum controlador é Principal. Promovendo Controlador 1...")
        controlador1.assumir_principal()

        return controlador1


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
