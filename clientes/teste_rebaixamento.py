import Pyro5.api

URI = "PYRO:controlador1@localhost:50001"

controlador = Pyro5.api.Proxy(URI)

print("Papel inicial:", controlador.obter_papel())

resultado = controlador.assumir_reserva()

print(resultado)
print("Papel atual:", controlador.obter_papel())

controlador._pyroRelease()