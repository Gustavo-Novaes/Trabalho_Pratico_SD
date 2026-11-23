import sqlite3
from pathlib import Path

import Pyro5.api


# Caminho do banco de dados do controlador 2
PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = PASTA_PROJETO / "banco_dados" / "controlador2.db"


@Pyro5.api.expose
class Controlador2:
    def __init__(self):
        self.papel = "Reserva"

    def obter_papel(self):
        return self.papel

    def assumir_principal(self):
        self.papel = "Principal"
        return "Controlador 2 agora é Principal."

    def obter_status(self):
        return "Controlador 2 funcionando!"

    def listar_obras(self):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.row_factory = sqlite3.Row

        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM obras")

        obras = [dict(registro) for registro in cursor.fetchall()]

        conexao.close()

        return obras

    def cadastrar_obra(self, nome, localizacao, descricao, data_inicio, status):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.execute("PRAGMA foreign_keys = ON")

        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO obras (
                nome, localizacao, descricao, data_inicio, status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (nome, localizacao, descricao, data_inicio, status))

        id_obra = cursor.lastrowid

        conexao.commit()
        conexao.close()

        # Tenta replicar a obra no Controlador 1
        try:
            controlador1 = Pyro5.api.Proxy(
                "PYRO:controlador1@localhost:50001"
            )

            resultado = controlador1.registrar_obra_replica(
                id_obra,
                nome,
                localizacao,
                descricao,
                data_inicio,
                status
            )

            controlador1._pyroRelease()

            return {
                "sucesso": True,
                "mensagem": "Obra cadastrada e replicada com sucesso!",
                "id_obra": id_obra,
                "replicacao": resultado
            }

        except Exception as erro:
            return {
                "sucesso": True,
                "mensagem": "Obra cadastrada no Controlador 2. A replicação está pendente.",
                "id_obra": id_obra,
                "erro": str(erro)
            }
    
    def registrar_obra_replica(self, id_obra, nome, localizacao, descricao, data_inicio, status):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.execute("PRAGMA foreign_keys = ON")

        cursor = conexao.cursor()

        # Verifica se a obra já existe
        cursor.execute(
            "SELECT id_obra FROM obras WHERE id_obra = ?",
            (id_obra,)
        )

        obra_existente = cursor.fetchone()

        if obra_existente:
            conexao.close()
            return "Obra já estava replicada!"

        # Insere a obra caso ainda não exista
        cursor.execute("""
            INSERT INTO obras (
                id_obra, nome, localizacao, descricao, data_inicio, status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_obra, nome, localizacao, descricao, data_inicio, status))

        conexao.commit()
        conexao.close()

        return "Obra replicada com sucesso!"
    
    def verificar_disponibilidade(self):
        return {
            "controlador": "Controlador 2",
            "disponivel": True
        }

    def assumir_reserva(self):
        self.papel = "Reserva"
        return "Controlador 2 agora é Reserva."

if __name__ == "__main__":
    controlador = Controlador2()

    daemon = Pyro5.api.Daemon(
        host="localhost",
        port=50002
    )

    uri = daemon.register(
        controlador,
        objectId="controlador2"
    )

    print("Controlador 2 iniciado!")
    print(f"Endereço: {uri}")

    daemon.requestLoop()
